from pathlib import Path

import pandas as pd
import requests

RAW_DATA_DIR = Path("data/raw")

# AMFI scheme codes provided by Bluestock
scheme_codes = [
    125497,
    119551,
    120503,
    118632,
    119092,
    120841
]
print("Validating Bluestock scheme codes against live MFAPI...\n")

for scheme_code in scheme_codes:
    api_url = f"https://api.mfapi.in/mf/{scheme_code}"

    response = requests.get(api_url, timeout=30)
    nav_json = response.json()

    meta = nav_json.get("meta", {})

    print("-" * 60)
    print("Requested Code:", scheme_code)
    print("API Fund House:", meta.get("fund_house"))
    print("API Scheme Name:", meta.get("scheme_name"))

    print("\n" + "=" * 70)
print("CHECKING CODES AGAINST BLUESTOCK FUND MASTER")
print("=" * 70)

fund_master = pd.read_csv(RAW_DATA_DIR / "01_fund_master.csv")

for scheme_code in scheme_codes:
    match = fund_master[fund_master["amfi_code"] == scheme_code]

    print(f"\nAMFI Code: {scheme_code}")

    if not match.empty:
        print("Bluestock Fund House:", match.iloc[0]["fund_house"])
        print("Bluestock Scheme Name:", match.iloc[0]["scheme_name"])
    else:
        print("Code not found in Bluestock fund master.")

print("\n" + "=" * 70)
print("SAVING LIVE NAV DATA")
print("=" * 70)

for scheme_code in scheme_codes:
    api_url = f"https://api.mfapi.in/mf/{scheme_code}"

    response = requests.get(api_url, timeout=30)
    response.raise_for_status()

    nav_json = response.json()
    meta = nav_json.get("meta", {})
    nav_data = nav_json.get("data", [])

    if not nav_data:
        print(f"No NAV data returned for {scheme_code}")
        continue

    df_nav = pd.DataFrame(nav_data)

    # Preserve the actual metadata returned by the API
    df_nav["amfi_code"] = meta.get("scheme_code")
    df_nav["scheme_name"] = meta.get("scheme_name")
    df_nav["fund_house"] = meta.get("fund_house")

    output_file = RAW_DATA_DIR / f"live_nav_{scheme_code}.csv"

    df_nav.to_csv(output_file, index=False)

    print(f"Saved: {output_file.name} | Rows: {len(df_nav)}")