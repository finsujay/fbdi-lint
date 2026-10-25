"""fbdi-lint: pre-flight checks for AP invoice FBDI files."""
import csv
import sys

REQUIRED_COLUMNS = [
    "INVOICE_NUM",
    "VENDOR_NAME",
    "INVOICE_AMOUNT",
    "INVOICE_DATE",
    "INVOICE_CURRENCY",
]


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

def main():
    if len(sys.argv) != 2:
        print("usage: python fbdi_lint.py <invoices.csv>")
        return 1
    missing = check_columns(sys.argv[1])
    if missing:
        print("MISSING COLUMNS: " + ", ".join(missing))
        return 1
    print("OK: all required columns present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
