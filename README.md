# Text-to-SQL Claims Analyst Agent

A beginner-friendly agentic AI project for a Business/Data Analyst portfolio.

**What it does:** you type a question in plain English about a (fake, synthetic)
health insurance claims dataset. Claude converts your question into SQL, the
script runs that SQL against a local database, and Claude then explains the
results in plain English — like a data analyst would explain a number to a
business stakeholder.

This directly demonstrates: SQL fluency, working with an LLM API, basic
agentic design (the model reasons, calls a "tool" — the database — and
responds), and safe handling of AI-generated code (it will only ever run
SELECT statements).

---

## Part 1: One-time Mac setup

### 1. Check if Python is already installed
Open **Terminal** (press `Cmd + Space`, type "Terminal", hit Enter), then run:

```
python3 --version
```

If you see something like `Python 3.11.x` or higher, skip to Step 2.
If you get an error, install Python:

- Go to https://www.python.org/downloads/macos/
- Download the latest macOS installer (the `.pkg` file)
- Run it and click through the installer (defaults are fine)
- Close and reopen Terminal, then run `python3 --version` again to confirm

### 2. Install a code editor (optional but recommended)
Download **VS Code**: https://code.visualstudio.com/download → the Mac version.
Drag it into your Applications folder. When you open a `.py` file in it for the
first time, it'll prompt you to install the Python extension — accept that.

You don't strictly need this; you can edit files in Terminal with `nano` or
TextEdit too. But VS Code makes reading/editing code much easier.

### 3. Get an Anthropic API key
1. Go to https://console.anthropic.com
2. Sign in / create an account
3. Go to **Settings → API Keys**
4. Click **Create Key**, name it something like `text-to-sql-agent`
5. Copy the key (it starts with `sk-ant-...`) — you won't be able to see it again,
   so paste it somewhere temporary if needed

Note: this is a separate account/key from your normal claude.ai chat login.
The API is billed separately (pay-as-you-go, based on usage) — for a project
this size, testing will cost a small fraction of a dollar.

---

## Part 2: Project setup (do this once per project)

### 1. Unzip / place the project folder
Put the `text-to-sql-agent` folder somewhere easy to find, e.g. your Desktop
or a `Projects` folder in your home directory.

### 2. Open Terminal in the project folder
Easiest way: in Finder, right-click the `text-to-sql-agent` folder →
**New Terminal at Folder**. (If you don't see that option, open Terminal
normally and use `cd` to navigate, e.g. `cd ~/Desktop/text-to-sql-agent`.)

### 3. Create a virtual environment
This keeps this project's Python packages separate from everything else on
your machine.

```
python3 -m venv venv
```

### 4. Activate the virtual environment

```
source venv/bin/activate
```

Your terminal prompt should now show `(venv)` at the start of the line. You'll
need to run this activate command again every time you open a new Terminal
window to work on this project.

### 5. Install the required packages

```
pip install -r requirements.txt
```

This installs three things: `anthropic` (Claude's API library), `pandas`
(for handling query results as tables), and `python-dotenv` (for loading
your API key from a file instead of pasting it into code).

### 6. Add your API key
Rename `.env.example` to `.env`:

```
mv .env.example .env
```

Then open `.env` in VS Code (or `nano .env` in Terminal) and replace
`your-key-here` with the real key you copied from the Anthropic console.
Save the file. **Never share this file or commit it to GitHub** — it's your
private credential.

---

## Part 3: Run it

### 1. Build the database (run once)

```
python3 setup_database.py
```

This creates `claims.db` — a SQLite file with 800 rows of fake insurance
claims (provider, region, date, amount, status, diagnosis code).

### 2. Start the agent

```
python3 agent.py
```

Try questions like:
- `What is the total claim amount by region?`
- `Which provider has the most denied claims?`
- `Show me the average claim amount for each diagnosis code`
- `How many claims were filed in the Lowcountry region in 2025?`

Type `exit` to quit.

For each question, you'll see: the SQL Claude generated, the raw results
table, and a plain-English summary.

---

## Troubleshooting

**"command not found: python3"** — Python isn't installed or Terminal needs
to be restarted. Reinstall from python.org and reopen Terminal.

**"No module named anthropic" (or pandas/dotenv)** — your virtual environment
isn't activated. Run `source venv/bin/activate` again (you should see `(venv)`
in your prompt), then reinstall with `pip install -r requirements.txt`.

**"Error code: 401" / authentication error** — your API key in `.env` is
missing, wrong, or the file wasn't renamed from `.env.example` to `.env`.

**"claims.db not found"** — run `python3 setup_database.py` before `python3 agent.py`.

---

## Ideas to extend this for your resume

- Swap the synthetic claims data for a real public dataset (Kaggle has several
  insurance/healthcare claims datasets) and adjust the schema/columns.
- Add a simple Streamlit front end so it's a clickable web app instead of a
  terminal tool.
- Add a basic anomaly-detection step (e.g. flag claims more than 3 standard
  deviations above the mean) before summarizing — ties directly into modeling.
- Push it to a public GitHub repo with this README as-is — it already explains
  the architecture and setup, which is exactly what hiring managers look for.
