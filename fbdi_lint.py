"""fbdi-lint: pre-flight checks for AP invoice FBDI files."""
import csv
import sys

REQUIRED_COLUMNS = [
    "INVOICE_NUM",
    "VENDOR_NAME",
    "INVOICE_AMOUNT",
    "INVOICE_DATE",
    "INVOICE_CURRENCY",
    "INVOICE_TYPE",
    "LEGAL_ENTITY",
]

def check_dates(path):
    """Return row numbers whose INVOICE_DATE is not in YYYY-MM-DD form."""
    bad = []
    with open(path, newline="") as f:
        for i, row in enumerate(csv.DictReader(f), start=2):
            parts = row.get("INVOICE_DATE", "").split("-")
            if len(parts) != 3 or len(parts[0]) != 4:
                bad.append(str(i))
    return bad

def check_columns(path):
    """Return the required columns missing from the CSV header."""
    with open(path, newline="") as f:
        header = next(csv.reader(f), [])
    return [c for c in REQUIRED_COLUMNS if c not in header]

def find_duplicates(path):
    """Return invoice numbers that appear more than once."""
    seen = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            num = row.get("INVOICE_NUM", "")
            seen[num] = seen.get(num, 0) + 1
    return [n for n, count in sorted(seen.items()) if count > 1]

def check_amounts(path):
    """Return row numbers whose INVOICE_AMOUNT is not a positive number."""
    bad = []
    with open(path, newline="") as f:
        for i, row in enumerate(csv.DictReader(f), start=2):
            try:
                if float(row.get("INVOICE_AMOUNT", "")) <= 0:
                    bad.append(str(i))
            except ValueError:
                bad.append(str(i))
    return bad

def main():
    if len(sys.argv) != 2:
        print("usage: python fbdi_lint.py <invoices.csv>")
        return 1
    missing = check_columns(sys.argv[1])
    if missing:
        print("MISSING COLUMNS: " + ", ".join(missing))
        return 1
    duplicates = find_duplicates(sys.argv[1])
    if duplicates:
        print("DUPLICATE INVOICE NUMBERS: " + ", ".join(duplicates))
        return 1
    bad_amounts = check_amounts(sys.argv[1])
    if bad_amounts:
        print("BAD AMOUNTS on rows: " + ", ".join(bad_amounts))
        return 1
    bad_dates = check_dates(sys.argv[1])
    if bad_dates:
        print("BAD DATES on rows: " + ", ".join(bad_dates))
        return 1

    print("OK: all required columns present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
