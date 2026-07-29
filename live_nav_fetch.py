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
# Load Bluestock fund master for scheme-code validation
fund_master = pd.read_csv(RAW_DATA_DIR / "01_fund_master.csv")

print("Fetching and validating live NAV data...\n")
for scheme_code in scheme_codes:
    api_url = f"https://api.mfapi.in/mf/{scheme_code}"

    print("-" * 70)
    print(f"Processing AMFI code: {scheme_code}")

    try:
        # Fetch data from MFAPI
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()

        nav_json = response.json()

        meta = nav_json.get("meta", {})
        nav_data = nav_json.get("data", [])

        if not nav_data:
            print("WARNING: No NAV records returned.")
            continue

        # Display actual API metadata
        print("API Fund House:", meta.get("fund_house"))
        print("API Scheme Name:", meta.get("scheme_name"))

    except requests.RequestException as error:
        print(f"API request failed: {error}")
        continue

    except ValueError as error:
        print(f"Invalid JSON response: {error}")
        continue
        # Compare with Bluestock fund master
    match = fund_master[fund_master["amfi_code"] == scheme_code]

    if not match.empty:
        bluestock_fund_house = match.iloc[0]["fund_house"]
        bluestock_scheme_name = match.iloc[0]["scheme_name"]

        print("Bluestock Fund House:", bluestock_fund_house)
        print("Bluestock Scheme Name:", bluestock_scheme_name)

        api_scheme_name = meta.get("scheme_name")

        if bluestock_scheme_name != api_scheme_name:
            print("WARNING: Bluestock and MFAPI scheme names do not match.")
    else:
        print("WARNING: AMFI code not found in Bluestock fund master.")

    # Convert NAV records to DataFrame
    df_nav = pd.DataFrame(nav_data)

    # Preserve metadata exactly as returned by the API
    df_nav["amfi_code"] = meta.get("scheme_code")
    df_nav["scheme_name"] = meta.get("scheme_name")
    df_nav["fund_house"] = meta.get("fund_house")

    # Save raw API data
    output_file = RAW_DATA_DIR / f"live_nav_{scheme_code}.csv"
    df_nav.to_csv(output_file, index=False)

    print(f"Saved: {output_file.name}")
    print(f"NAV records: {len(df_nav)}")