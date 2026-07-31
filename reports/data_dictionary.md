# Mutual Fund Analytics Data Dictionary

## Table: nav_history

| Column | Data Type | Description |
|--------|-----------|-------------|
| amfi_code | INTEGER | Unique AMFI code identifying the mutual fund scheme |
| date | DATE | Date of the NAV record |
| nav | REAL | Net Asset Value (NAV) of the scheme |

---

## Table: investor_transactions

| Column | Data Type | Description |
|--------|-----------|-------------|
| investor_id | TEXT | Unique investor identifier |
| transaction_date | DATE | Date of the transaction |
| amfi_code | INTEGER | AMFI code of the mutual fund scheme |
| transaction_type | TEXT | Type of transaction (SIP, Lumpsum, Redemption) |
| amount_inr | INTEGER | Transaction amount in Indian Rupees |
| state | TEXT | State of the investor |
| city | TEXT | City of the investor |
| city_tier | TEXT | City classification (T30/B30) |
| age_group | TEXT | Investor age group |
| gender | TEXT | Investor gender |
| annual_income_lakh | REAL | Annual income in lakhs |
| payment_mode | TEXT | Mode of payment |
| kyc_status | TEXT | KYC verification status |

---

## Table: scheme_performance

| Column | Data Type | Description |
|--------|-----------|-------------|
| amfi_code | INTEGER | Unique AMFI code identifying the scheme |
| scheme_name | TEXT | Name of the mutual fund scheme |
| fund_house | TEXT | Asset Management Company (AMC) |
| category | TEXT | Fund category |
| plan | TEXT | Direct or Regular plan |
| return_1yr_pct | REAL | 1-year return (%) |
| return_3yr_pct | REAL | 3-year return (%) |
| return_5yr_pct | REAL | 5-year return (%) |
| benchmark_3yr_pct | REAL | 3-year benchmark return (%) |
| alpha | REAL | Alpha performance metric |
| beta | REAL | Beta risk metric |
| sharpe_ratio | REAL | Sharpe ratio |
| sortino_ratio | REAL | Sortino ratio |
| std_dev_ann_pct | REAL | Annualized standard deviation (%) |
| max_drawdown_pct | REAL | Maximum drawdown (%) |
| aum_crore | INTEGER | Assets Under Management (₹ Crore) |
| expense_ratio_pct | REAL | Expense ratio (%) |
| morningstar_rating | INTEGER | Morningstar rating |
| risk_grade | TEXT | Risk category of the scheme |