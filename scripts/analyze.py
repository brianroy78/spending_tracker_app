from datetime import datetime, timedelta
from functools import partial
from operator import attrgetter

import database as db
from core.functors import IterFunctor
from core.models import Category
from database.models import TransactionTable, CategoryTable


def get_transactions(session, start: datetime, end: datetime) -> list[TransactionTable]:
    return (
        session.query(TransactionTable)
        .filter(TransactionTable.datetime.between(start, end + timedelta(days=1)))
        .order_by(TransactionTable.datetime.desc())
        .all()
    )


def match(key_texts: list[str], transaction: TransactionTable) -> bool:
    note = transaction.note.lower()
    for key_text in key_texts:
        if key_text in note:
            return True
    return False


def transform_to_category(transactions: list[TransactionTable], category: CategoryTable) -> Category:
    key_texts = IterFunctor(category.key_texts).map(attrgetter("text")).list()
    filter_ = partial(match, key_texts)

    return Category(
        name=category.name,
        key_texts=key_texts,
        transactions=IterFunctor(transactions).filter(filter_).list(),
    )


def run(from_: str, to: str):
    from_date = datetime.fromisoformat(from_)
    to_date = datetime.fromisoformat(to)
    session = db.connect_get_session()
    categories = session.query(CategoryTable).all()
    transactions = get_transactions(session, from_date, to_date)
    transform_ = partial(transform_to_category, transactions)
    results = IterFunctor(categories).map(transform_).list()
    for r in results:
        print(r.total_expenditure())
