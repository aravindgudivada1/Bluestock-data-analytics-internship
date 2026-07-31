import sqlite3
from pathlib import Path
import pandas as pd

# -----------------------------
# Project Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "mutual_fund_analytics.db"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# -----------------------------
# Connect to Database
# -----------------------------
conn = sqlite3.connect(DB_PATH)

# -----------------------------
# Read cleaned CSVs
# -----------------------------
nav = pd.read_csv(PROCESSED_DIR / "02_nav_history_cleaned.csv")

transactions = pd.read_csv(
    PROCESSED_DIR / "08_investor_transactions_cleaned.csv"
)

performance = pd.read_csv(
    PROCESSED_DIR / "07_scheme_performance_cleaned.csv"
)

# -----------------------------
# Load into SQLite
# -----------------------------
nav.to_sql("nav_history", conn, if_exists="replace", index=False)

transactions.to_sql(
    "investor_transactions",
    conn,
    if_exists="replace",
    index=False,
)

performance.to_sql(
    "scheme_performance",
    conn,
    if_exists="replace",
    index=False,
)

print("Data loaded successfully!")

# -----------------------------
# Verify row counts
# -----------------------------
tables = [
    "nav_history",
    "investor_transactions",
    "scheme_performance",
]

for table in tables:
    count = conn.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]
    print(f"{table}: {count:,} rows")

conn.close()