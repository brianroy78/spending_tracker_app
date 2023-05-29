from datetime import datetime, timedelta
from functools import partial
from operator import attrgetter

import database as db
from core import utils
from core.functors import IterFunctor
from database.models import TransactionTable, CategoryTable


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
        .all()
    )


def match2(key_texts: list[str], note: str) -> bool:
    for key_text in key_texts:
        if key_text in note:
            return True
    return False


def run(from_: str, to: str):
    from_date = datetime.fromisoformat(from_)
    to_date = datetime.fromisoformat(to)
    session = db.connect_get_session()
    categories = session.query(CategoryTable).all()
    for c in categories:
        transactions = get_transactions(session, from_date, to_date)
        filter_ = partial(match2, c.key_texts)
        r = Category(
            name=c.name,
            key_texts=IterFunctor(c.key_texts).map(attrgetter("text")).list(),
            transactions=IterFunctor(transactions).filter(filter_).list(),
        )

    unknown_category = Category(name=ExpenditureCategories.UNKNOWN.value, keywords=[], expenditure=0)
    for transaction in get_transactions(session, from_date, to_date):
        if transaction.is_entry:
            continue
        category = match(unknown_category, categories, str(transaction.note))
        category.expenditure += float(transaction.amount)
        print(transaction)
    for c in categories:
        print(f"{c.name} => {c.expenditure}")
    print(f"{unknown_category.name} => {unknown_category.expenditure}")
    print(f"total => {sum([c.expenditure for c in categories]) + unknown_category.expenditure}")
