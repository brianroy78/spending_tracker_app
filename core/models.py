import enum
from dataclasses import dataclass


class ExpenditureCategories(enum.Enum):
    ESSENTIALS = 'essentials'
    EATING_OUT = 'eating_out'
    ENTERTAINMENT = 'entertainment'
    HEALTH = 'health'
    CAR = 'car'
    GIFTS = 'gifts'
    CLOTHES = 'clothes'
    UNKNOWN = 'unknown'


@dataclass
class Category:
    name: str
    keywords: list[str]
    expenditure: float
