import sqlite3
from pathlib import Path

# -------------------------------------
# Project Paths
# -------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "mutual_fund_analytics.db"

# -------------------------------------
# Connect to SQLite
# -------------------------------------
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

queries = [

("Query 1 - Top 5 Funds by AUM", """
SELECT
    scheme_name,
    fund_house,
    aum_crore
FROM scheme_performance
ORDER BY aum_crore DESC
LIMIT 5;
"""),

("Query 2 - Average NAV Per Month", """
SELECT
    strftime('%Y-%m', date) AS month,
    ROUND(AVG(nav),2) AS average_nav
FROM nav_history
GROUP BY month
ORDER BY month;
"""),

("Query 3 - Transactions by State", """
SELECT
    state,
    COUNT(*) AS total_transactions,
    SUM(amount_inr) AS total_amount
FROM investor_transactions
GROUP BY state
ORDER BY total_amount DESC;
"""),

("Query 4 - Expense Ratio below 1%", """
SELECT
    scheme_name,
    fund_house,
    expense_ratio_pct
FROM scheme_performance
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct;
"""),

("Query 5 - Transaction Type Summary", """
SELECT
    transaction_type,
    COUNT(*) AS total_transactions,
    SUM(amount_inr) AS total_amount
FROM investor_transactions
GROUP BY transaction_type;
"""),

("Query 6 - Top 5 Performing Funds (3-Year Return)", """
SELECT
    scheme_name,
    return_3yr_pct
FROM scheme_performance
ORDER BY return_3yr_pct DESC
LIMIT 5;
"""),

("Query 7 - Average Transaction Amount by Gender", """
SELECT
    gender,
    ROUND(AVG(amount_inr),2) AS average_transaction
FROM investor_transactions
GROUP BY gender;
"""),

("Query 8 - KYC Status Distribution", """
SELECT
    kyc_status,
    COUNT(*) AS investors
FROM investor_transactions
GROUP BY kyc_status;
"""),

("Query 9 - Risk Grade Distribution", """
SELECT
    risk_grade,
    COUNT(*) AS total_funds
FROM scheme_performance
GROUP BY risk_grade;
"""),

("Query 10 - Average NAV by Fund", """
SELECT
    amfi_code,
    ROUND(AVG(nav),2) AS average_nav
FROM nav_history
GROUP BY amfi_code
ORDER BY average_nav DESC;
""")

]

for title, query in queries:

    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)

    try:
        rows = cursor.execute(query).fetchall()

        if not rows:
            print("No rows returned.")
            continue

        for row in rows[:10]:
            print(row)

        if len(rows) > 10:
            print(f"... ({len(rows)} rows returned)")

    except Exception as e:
        print("ERROR:", e)

conn.close()

print("\nAll queries executed.")