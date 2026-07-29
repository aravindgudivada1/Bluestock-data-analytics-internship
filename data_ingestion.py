from pathlib import Path
import pandas as pd


# Project data directory
RAW_DATA_DIR = Path("data/raw")

print("Raw data directory:", RAW_DATA_DIR)

# Discover all CSV files in the raw data directory
csv_files = sorted(RAW_DATA_DIR.glob("*.csv"))

print(f"\nTotal CSV files found: {len(csv_files)}")

for file in csv_files:
    print(file.name)

# Load and inspect each dataset
for file in csv_files:
    print("\n" + "=" * 80)
    print(f"DATASET: {file.name}")
    print("=" * 80)

    df = pd.read_csv(file)

    print("\nShape:")
    print(df.shape)

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 5 Rows:")
    print(df.head())
        # Basic data quality checks
    print("\nData Quality Checks:")

    missing_values = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()

    print(f"Missing values: {missing_values}")
    print(f"Duplicate rows: {duplicate_rows}")

    # Identify columns containing missing values
    missing_by_column = df.isnull().sum()
    missing_by_column = missing_by_column[missing_by_column > 0]

    if not missing_by_column.empty:
        print("\nColumns with missing values:")
        print(missing_by_column)
    else:
        print("No missing values detected.")
     