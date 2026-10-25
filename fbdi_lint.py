"""fbdi-lint: pre-flight checks for AP invoice FBDI files."""
import csv
import sys

REQUIRED_COLUMNS = [
    "INVOICE_NUM",
    "VENDOR_NAME",
    "INVOICE_AMOUNT",
    "INVOICE_DATE",
]


def check_columns(path):
    """Return the required columns missing from the CSV header."""
    with open(path, newline="") as f:
        header = next(csv.reader(f), [])
    return [c for c in REQUIRED_COLUMNS if c not in header]


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
