"""
pe3.py — Pair Exercise #3: Functions and Classes
Implementations match the provided tests in test_pe3.py.
"""

from __future__ import annotations

import string
import datetime
from dataclasses import dataclass

# ==========================
# Caesar cipher: encode/decode
# ==========================

def _shift_char(ch: str, shift: int) -> str:
    """Shift a single character within the lowercase alphabet; non-letters are returned unchanged.
    Always returns lowercase letters.
    """
    if ch.isalpha():
        # Work in lowercase only
        idx = string.ascii_lowercase.find(ch.lower())
        if idx != -1:
            return string.ascii_lowercase[(idx + shift) % 26]
    return ch


def encode(input_text: str, shift: int):
    """Return (alphabet_list, encoded_text) where alphabet_list == list(string.ascii_lowercase).
    Encoding is Caesar cipher with the given positive/negative shift. Output is lowercase.
    Non-letters (spaces, punctuation, digits) are left unchanged.
    """
    alphabet_list = list(string.ascii_lowercase)
    encoded = "".join(_shift_char(ch, shift) for ch in input_text)
    return (alphabet_list, encoded)


def decode(input_text: str, shift: int) -> str:
    """Return decoded text using Caesar cipher with the given shift.
    Output is lowercase; non-letters are left unchanged.
    """
    decoded = "".join(_shift_char(ch, -shift) for ch in input_text)
    return decoded


# ==========================
# Banking classes
# ==========================

@dataclass
class BankAccount:
    """Basic bank account.

    Rules (per assignment/tests):
      - creation_date must be a date that is not in the future (today OK).
      - Negative deposits are not allowed (ignored).
      - deposit/withdraw should display (print) resulting balance.
    """
    name: str = "Rainy"
    ID: str | int = "1234"
    creation_date: datetime.date = datetime.date.today()
    balance: float = 0

    def __post_init__(self):
        # Type check & future-date guard
        if not isinstance(self.creation_date, datetime.date):
            raise TypeError("creation_date must be a datetime.date")
        if self.creation_date > datetime.date.today():
            # Tests expect a generic Exception here
            raise Exception("creation_date cannot be in the future")

    # ----- Methods required by tests -----
    def deposit(self, amount: float) -> None:
        """Deposit a positive amount; negative amounts are ignored."""
        if amount is None:
            return
        try:
            amt = float(amount)
        except (TypeError, ValueError):
            return
        if amt > 0:
            self.balance += amt
        # "display" resulting balance
        print(f"Balance: {self.balance}")

    def withdraw(self, amount: float) -> None:
        """Withdraw the given amount (no overdraft restriction at base class)."""
        if amount is None:
            return
        try:
            amt = float(amount)
        except (TypeError, ValueError):
            return
        self.balance -= amt
        print(f"Balance: {self.balance}")

    def view_balance(self):
        """Return current balance."""
        return self.balance


class SavingsAccount(BankAccount):
    """Savings account:
        - No overdrafts permitted.
        - Withdrawals only after 180 days since creation.
    """
    MIN_AGE_DAYS = 180

    def _age_in_days(self) -> int:
        return (datetime.date.today() - self.creation_date).days

    def withdraw(self, amount: float) -> None:
        # Disallow if the account is younger than 180 days
        if self._age_in_days() < self.MIN_AGE_DAYS:
            print(f"Balance: {self.balance}")
            return
        # Disallow overdraft
        try:
            amt = float(amount)
        except (TypeError, ValueError):
            print(f"Balance: {self.balance}")
            return
        if amt <= self.balance:
            self.balance -= amt
        # "display" resulting balance regardless
        print(f"Balance: {self.balance}")


class CheckingAccount(BankAccount):
    """Checking account:
        - Overdrafts permitted, but each time a withdrawal causes
          a negative balance, apply a $30 fee.
    """
    OVERDRAFT_FEE = 30.0

    def withdraw(self, amount: float) -> None:
        try:
            amt = float(amount)
        except (TypeError, ValueError):
            print(f"Balance: {self.balance}")
            return
        pre = self.balance
        self.balance -= amt
        # If this withdrawal transitions balance to negative (strictly < 0),
        # apply overdraft fee.
        if pre >= 0 and self.balance < 0:
            self.balance -= self.OVERDRAFT_FEE
        print(f"Balance: {self.balance}")
