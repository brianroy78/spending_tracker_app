from datetime import date, datetime, timedelta

import database as db
from core.models import Category, ExpenditureCategories
from database.models import TransactionTable, CategoryTable
from core import utils


def match(unknown_category: Category, categories: list[Category], note: str) -> Category:
    for c in categories:
        if utils.is_empty(c.keywords):
            continue
        for word in c.keywords:
            if word in note.lower():
                return c
    return unknown_category


def get_transactions(session, start: datetime, end: datetime) -> list[TransactionTable]:
    return (
        session.query(TransactionTable)
        .filter(TransactionTable.datetime.between(start, end + timedelta(days=1)))
        .order_by(TransactionTable.datetime.desc())
    )


def run(from_: str, to: str):
    from_date = datetime.fromisoformat(from_)
    to_date = datetime.fromisoformat(to)
    session = db.connect_get_session()
    categories = [
        Category(
            name=c.name,
            keywords=c.keywords.split("|") if not utils.is_empty(c.keywords) else [],
            expenditure=0,
        )
        for c in session.query(CategoryTable)
    ]
    unknown_category = Category(name=ExpenditureCategories.UNKNOWN.value, keywords=[], expenditure=0)
    for transaction in get_transactions(session, from_date, to_date):
        if transaction.is_entry:
            continue
        category = match(unknown_category, categories, transaction.note)
        category.expenditure += transaction.amount
        print(transaction)
    for c in categories:
        print(f"{c.name} => {c.expenditure}")
    print(f"{unknown_category.name} => {unknown_category.expenditure}")
    print(f"total => {sum([c.expenditure for c in categories]) + unknown_category.expenditure}")
