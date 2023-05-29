from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    note: str
    amount: int
    is_entry: bool
    datetime: datetime
    method: str


@dataclass
class Category:
    name: str
    key_texts: list[str]
    transactions: list[Transaction]

    def total_expenditure(self) -> int:
        return sum([t.amount for t in self.transactions])
