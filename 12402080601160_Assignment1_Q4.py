"""
Q4 - Exception-Safe CSV Transaction Splitter
Usage:
    python Q4_csv_transaction_splitter.py transactions.csv
Creates credit.csv, debit.csv and error.csv in the current directory.
"""
import csv
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


REQUIRED = ["transaction_id", "account_id", "type", "amount", "timestamp"]


def validate(row):
    missing = [field for field in REQUIRED if field not in row]
    if missing:
        raise ValueError("missing column(s): " + ", ".join(missing))

    if not row["transaction_id"] or not row["account_id"]:
        raise ValueError("transaction_id/account_id cannot be empty")

    tx_type = row["type"].strip().upper()
    if tx_type not in {"CREDIT", "DEBIT"}:
        raise ValueError("type must be CREDIT or DEBIT")

    amount = float(row["amount"])
    if amount <= 0:
        raise ValueError("amount must be greater than zero")

    datetime.strptime(row["timestamp"], "%Y-%m-%dT%H:%M:%S")
    return tx_type, amount


def process_file(input_path):
    balances = defaultdict(float)

    with open(input_path, newline="", encoding="utf-8") as src:
        reader = csv.DictReader(src)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header.")

        fieldnames = list(reader.fieldnames)
        for field in REQUIRED:
            if field not in fieldnames:
                raise ValueError(f"Missing required column: {field}")

        with open("credit.csv", "w", newline="", encoding="utf-8") as credit_f, \
             open("debit.csv", "w", newline="", encoding="utf-8") as debit_f, \
             open("error.csv", "w", newline="", encoding="utf-8") as error_f:

            credit_writer = csv.DictWriter(credit_f, fieldnames=fieldnames)
            debit_writer = csv.DictWriter(debit_f, fieldnames=fieldnames)
            error_fields = fieldnames + ["reason"]
            error_writer = csv.DictWriter(error_f, fieldnames=error_fields)

            credit_writer.writeheader()
            debit_writer.writeheader()
            error_writer.writeheader()

            for row in reader:
                try:
                    tx_type, amount = validate(row)
                    if tx_type == "CREDIT":
                        credit_writer.writerow(row)
                        balances[row["account_id"]] += amount
                    else:
                        debit_writer.writerow(row)
                        balances[row["account_id"]] -= amount
                except (ValueError, TypeError) as exc:
                    error_writer.writerow({**row, "reason": str(exc)})

    print("Account-wise net balance change:")
    for account, balance in sorted(
        balances.items(), key=lambda item: (-abs(item[1]), item[0])
    ):
        value = int(balance) if balance.is_integer() else balance
        print(account, value)

    print("Files created: credit.csv, debit.csv, error.csv")


def main():
    if len(sys.argv) != 2:
        print("Usage: python Q4_csv_transaction_splitter.py transactions.csv")
        sys.exit(1)

    try:
        process_file(Path(sys.argv[1]))
    except (OSError, ValueError) as exc:
        print(f"INPUT_ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
