"""
setup_database.py

Creates a small SQLite database (claims.db) with synthetic health insurance
claims data. This is fake data, generated randomly - safe to use in a
portfolio project.

Run this once before running agent.py:
    python setup_database.py
"""

import sqlite3
import random
from datetime import date, timedelta

DB_NAME = "claims.db"

PROVIDERS = [
    "Palmetto Health Clinic", "Midlands Family Practice", "Carolina Ortho Group",
    "Lakeview Pediatrics", "Summit Cardiology", "Riverside Urgent Care",
    "Greenway Dermatology", "Trinity Physical Therapy",
]

REGIONS = ["Upstate", "Midlands", "Lowcountry", "Pee Dee"]

DIAGNOSIS_CODES = ["E11.9", "I10", "J06.9", "M54.5", "K21.9", "F41.1", "Z00.00", "R51"]

STATUSES = ["Paid", "Denied", "Pending"]
STATUS_WEIGHTS = [0.75, 0.15, 0.10]  # most claims paid, some denied, few pending


def random_date(start: date, end: date) -> date:
    delta_days = (end - start).days
    return start + timedelta(days=random.randint(0, delta_days))


def build_database(num_claims: int = 800):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS claims")
    cur.execute("""
        CREATE TABLE claims (
            claim_id INTEGER PRIMARY KEY,
            member_id INTEGER NOT NULL,
            provider_name TEXT NOT NULL,
            region TEXT NOT NULL,
            service_date TEXT NOT NULL,
            diagnosis_code TEXT NOT NULL,
            claim_amount REAL NOT NULL,
            claim_status TEXT NOT NULL
        )
    """)

    start = date(2025, 1, 1)
    end = date(2026, 6, 30)

    rows = []
    for claim_id in range(1, num_claims + 1):
        member_id = random.randint(10000, 10500)
        provider = random.choice(PROVIDERS)
        region = random.choice(REGIONS)
        service_date = random_date(start, end).isoformat()
        diagnosis = random.choice(DIAGNOSIS_CODES)
        amount = round(random.uniform(60, 4500), 2)
        status = random.choices(STATUSES, weights=STATUS_WEIGHTS, k=1)[0]
        rows.append((claim_id, member_id, provider, region, service_date, diagnosis, amount, status))

    cur.executemany(
        "INSERT INTO claims VALUES (?, ?, ?, ?, ?, ?, ?, ?)", rows
    )

    conn.commit()
    conn.close()
    print(f"Created {DB_NAME} with {num_claims} synthetic claims.")


if __name__ == "__main__":
    build_database()
