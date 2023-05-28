from dataclasses import dataclass


@dataclass
class Category:
    name: str
    key_texts: list[str]
    expenditure: int
