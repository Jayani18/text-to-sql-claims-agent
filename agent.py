"""
agent.py

A basic Text-to-SQL analyst agent.

You ask a question in plain English about the claims data, and this script:
  1. Sends your question + the database schema to Claude
  2. Gets back a SQL query
  3. Runs that query against claims.db
  4. Asks Claude to summarize the results in plain English

Run:
    python agent.py
"""

import os
import sqlite3
import sys

import pandas as pd
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()  # reads ANTHROPIC_API_KEY from a .env file in this folder

DB_NAME = "claims.db"
MODEL = "claude-haiku-4-5-20251001"  # fast + cheap; swap to "claude-sonnet-5" for tougher questions

client = Anthropic()  # automatically picks up ANTHROPIC_API_KEY from the environment


def get_schema(conn: sqlite3.Connection) -> str:
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(claims)")
    columns = cur.fetchall()
    col_lines = "\n".join(f"  - {col[1]} ({col[2]})" for col in columns)
    return f"Table: claims\nColumns:\n{col_lines}"


def question_to_sql(question: str, schema: str) -> str:
    system_prompt = f"""You are a SQL expert working with a SQLite database.

Here is the schema:
{schema}

Convert the user's question into a single valid SQLite SELECT query.
Rules:
- Only output the raw SQL query, nothing else. No explanation, no markdown fences.
- Only ever write SELECT statements. Never write INSERT, UPDATE, DELETE, or DROP.
- Use the exact column and table names from the schema.
- When comparing text values (like status, region, or provider names), always match case-insensitively, for example using COLLATE NOCASE, since you can't know the exact capitalization of the data.
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=system_prompt,
        messages=[{"role": "user", "content": question}],
    )
    sql = response.content[0].text.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql


def summarize_results(question: str, sql: str, df: pd.DataFrame) -> str:
    if df.empty:
        results_text = "The query returned no rows."
    else:
        results_text = df.head(20).to_string(index=False)

    prompt = f"""A user asked: "{question}"

This SQL query was run:
{sql}

Here are the results (up to 20 rows):
{results_text}

Write a short, plain-English summary (2-4 sentences) of what this tells the user,
as if you were a data analyst explaining it to a business stakeholder.
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()


def run_query(conn: sqlite3.Connection, sql: str) -> pd.DataFrame:
    if not sql.strip().upper().startswith("SELECT"):
        raise ValueError("Refusing to run a non-SELECT query for safety.")
    return pd.read_sql_query(sql, conn)


def main():
    if not os.path.exists(DB_NAME):
        print(f"{DB_NAME} not found. Run 'python setup_database.py' first.")
        sys.exit(1)

    conn = sqlite3.connect(DB_NAME)
    schema = get_schema(conn)

    print("Text-to-SQL Claims Analyst Agent")
    print("Type a question about the claims data, or 'exit' to quit.\n")
    print("Example: 'What is the total claim amount by region for denied claims?'\n")

    while True:
        question = input("Your question: ").strip()
        if question.lower() in ("exit", "quit"):
            break
        if not question:
            continue

        try:
            sql = question_to_sql(question, schema)
            print(f"\nGenerated SQL:\n  {sql}\n")

            df = run_query(conn, sql)
            print("Results:")
            print(df.head(20).to_string(index=False) if not df.empty else "(no rows)")

            summary = summarize_results(question, sql, df)
            print(f"\nSummary: {summary}\n")

        except Exception as e:
            print(f"Something went wrong: {e}\n")

    conn.close()
    print("Goodbye!")


if __name__ == "__main__":
    main()
