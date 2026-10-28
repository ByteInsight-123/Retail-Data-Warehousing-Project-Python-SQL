import sys
import pandas as pd

CSV_PATH = "data/Sample - Superstore.csv"

REQUIRED_COLUMNS = [
    "Order ID", "Order Date", "Ship Date", "Ship Mode", "Customer ID",
    "Customer Name", "Segment", "Postal Code", "City", "State", "Region",
    "Country", "Product ID", "Product Name", "Category", "Sub-Category",
    "Sales", "Quantity", "Discount", "Profit",
]

results = []


def record(status, name, detail=""):
    results.append(status)
    line = f"[{status}] {name}"
    if detail:
        line += f" -> {detail}"
    print(line)


def load_data(path):
    try:
        return pd.read_csv(path, encoding="latin1")
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="utf-8")


def run_checks(df):
    # 1. All columns we need are present
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        record("FAIL", "Required columns present", f"missing: {missing_cols}")
        return  # no point continuing
    record("PASS", "Required columns present")

    # 2. No fully duplicate rows
    dups = int(df.duplicated().sum())
    record("PASS" if dups == 0 else "FAIL", "No duplicate rows", f"{dups} found")

    # 3. No missing values in the columns we use
    nulls = int(df[REQUIRED_COLUMNS].isna().sum().sum())
    record("PASS" if nulls == 0 else "FAIL", "No missing values", f"{nulls} found")

    # 4. Dates can be read, and shipping is not before ordering
    order = pd.to_datetime(df["Order Date"], format="%m/%d/%Y", errors="coerce")
    ship = pd.to_datetime(df["Ship Date"], format="%m/%d/%Y", errors="coerce")
    bad_dates = int(order.isna().sum() + ship.isna().sum())
    record("PASS" if bad_dates == 0 else "FAIL", "Dates are valid", f"{bad_dates} unreadable")
    early = int((ship < order).sum())
    record("PASS" if early == 0 else "FAIL", "Ship date not before order date", f"{early} rows")

    # 5. Numbers make sense
    record("PASS" if (df["Sales"] >= 0).all() else "FAIL", "Sales is not negative")
    record("PASS" if (df["Quantity"] > 0).all() else "FAIL", "Quantity is above zero")
    ok_disc = df["Discount"].between(0, 1).all()
    record("PASS" if ok_disc else "FAIL", "Discount is between 0 and 1")

    # 6. Lookup keys: one ID should mean one name (WARN, not FAIL)
    cust = int((df.groupby("Customer ID")["Customer Name"].nunique() > 1).sum())
    record("PASS" if cust == 0 else "WARN", "Each Customer ID has one name", f"{cust} IDs differ")
    prod = int((df.groupby("Product ID")["Product Name"].nunique() > 1).sum())
    record("PASS" if prod == 0 else "WARN", "Each Product ID has one name", f"{prod} IDs differ")
    place = df.groupby("Postal Code")[["City", "State"]].nunique()
    place_bad = int((place > 1).any(axis=1).sum())
    record("PASS" if place_bad == 0 else "WARN", "Each Postal Code has one city/state", f"{place_bad} codes differ")


if __name__ == "__main__":
    data = load_data(CSV_PATH)
    print(f"Checking {len(data)} rows from {CSV_PATH}\n")
    run_checks(data)
    print(f"\nSummary: {results.count('PASS')} passed, "
          f"{results.count('WARN')} warnings, {results.count('FAIL')} failed")
    sys.exit(1 if "FAIL" in results else 0)