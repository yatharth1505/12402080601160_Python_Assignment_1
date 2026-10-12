"""
Q5 - Object-Oriented Bank Settlement System
Supports deposits, withdrawals, transfers, transaction history and
atomic BATCH_BEGIN/BATCH_END rollback.
"""
import sys
from dataclasses import dataclass


class BankError(Exception):
    """Base exception for bank errors."""


class AccountNotFoundError(BankError):
    pass


class InvalidAmountError(BankError):
    pass


class InsufficientFundsError(BankError):
    pass


@dataclass(frozen=True)
class Transaction:
    kind: str
    source: str | None
    target: str | None
    amount: int


class Account:
    def __init__(self, account_id, balance=0):
        if balance < 0:
            raise InvalidAmountError("Initial balance cannot be negative.")
        self._account_id = account_id
        self._balance = balance
        self._history = []

    @property
    def account_id(self):
        return self._account_id

    @property
    def balance(self):
        return self._balance

    @property
    def history(self):
        return tuple(self._history)

    def _change(self, delta):
        new_balance = self._balance + delta
        if new_balance < 0:
            raise InsufficientFundsError(
                f"Insufficient funds in account {self._account_id}."
            )
        self._balance = new_balance

    def record(self, transaction):
        self._history.append(transaction)


class Bank:
    def __init__(self, accounts):
        self.accounts = accounts
        self.failed_batches = []

    def get(self, account_id):
        if account_id not in self.accounts:
            raise AccountNotFoundError(f"Unknown account: {account_id}")
        return self.accounts[account_id]

    @staticmethod
    def validate_amount(amount):
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive.")

    def deposit(self, account_id, amount):
        self.validate_amount(amount)
        acc = self.get(account_id)
        acc._change(amount)
        acc.record(Transaction("DEPOSIT", None, account_id, amount))

    def withdraw(self, account_id, amount):
        self.validate_amount(amount)
        acc = self.get(account_id)
        acc._change(-amount)
        acc.record(Transaction("WITHDRAW", account_id, None, amount))

    def transfer(self, source, target, amount):
        self.validate_amount(amount)
        if source == target:
            raise BankError("Source and target must differ.")
        src = self.get(source)
        dst = self.get(target)
        src._change(-amount)
        dst._change(amount)
        tx = Transaction("TRANSFER", source, target, amount)
        src.record(tx)
        dst.record(tx)


def run(data):
    lines = [x.strip() for x in data.splitlines() if x.strip()]
    pos = 0

    n = int(lines[pos])
    pos += 1
    accounts = {}
    for _ in range(n):
        account_id, balance = lines[pos].split()
        pos += 1
        accounts[account_id] = Account(account_id, int(balance))

    q = int(lines[pos])
    pos += 1
    if len(lines) - pos < q:
        raise ValueError("Not enough operations.")

    bank = Bank(accounts)
    batch_snapshot = None
    batch_number = 0

    for operation in lines[pos:pos + q]:
        parts = operation.split()
        command = parts[0]

        if command == "BATCH_BEGIN":
            if batch_snapshot is not None:
                raise BankError("Nested batches are not supported.")
            batch_number += 1
            batch_snapshot = {
                acc_id: acc.balance for acc_id, acc in bank.accounts.items()
            }
            continue

        if command == "BATCH_END":
            if batch_snapshot is None:
                raise BankError("BATCH_END without BATCH_BEGIN.")
            batch_snapshot = None
            continue

        # Once a batch has failed, later operations in that batch are ignored
        # until BATCH_END; the original balances have already been restored.
        if batch_snapshot is not None and batch_number in bank.failed_batches:
            continue

        try:
            if command == "DEPOSIT" and len(parts) == 3:
                bank.deposit(parts[1], int(parts[2]))
            elif command == "WITHDRAW" and len(parts) == 3:
                bank.withdraw(parts[1], int(parts[2]))
            elif command == "TRANSFER" and len(parts) == 4:
                bank.transfer(parts[1], parts[2], int(parts[3]))
            else:
                raise BankError("Invalid operation format.")
        except (BankError, ValueError) as exc:
            if batch_snapshot is not None:
                # Mark the current batch as failed, restore its starting state,
                # and ignore later mutations until BATCH_END.
                for acc_id, balance in batch_snapshot.items():
                    bank.accounts[acc_id]._balance = balance
                if batch_number not in bank.failed_batches:
                    bank.failed_batches.append(batch_number)
                # Keep the snapshot active so BATCH_END closes the failed batch.
            else:
                # Non-batch operation failures do not alter account state.
                print(f"FAILED_OPERATION {operation}: {exc}", file=sys.stderr)

    output = []
    for failed in bank.failed_batches:
        output.append(f"FAILED {failed}")

    for account_id in sorted(bank.accounts):
        output.append(f"{account_id} {bank.accounts[account_id].balance}")

    return "\n".join(output)


def main():
    try:
        print(run(sys.stdin.read()))
    except (ValueError, BankError) as exc:
        print(f"INPUT_ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
