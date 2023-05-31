from datetime import datetime, timedelta
from functools import partial, reduce
from operator import attrgetter, iadd

from sqlalchemy.orm import selectinload

import database as db
from core.functors import IterFunctor
from core.models import Category
from core.utils import is_empty
from database.models import TransactionTable, CategoryTable, TransactionDetailTable


def get_transactions(session, start: datetime, end: datetime) -> list[TransactionTable]:
    return (
        session.query(TransactionTable)
        .options(
            selectinload(TransactionTable.details),
            selectinload(TransactionTable.details, TransactionDetailTable.category),
        )
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


def flat_transaction(transaction: TransactionTable) -> list[TransactionTable]:
    if is_empty(transaction.details):
        return [transaction]
    remaining_amount = transaction.amount
    new_transactions: list[TransactionTable] = []
    for detail in transaction.details:
        new_transactions.append(
            TransactionTable(
                note=transaction.note,
                amount=transaction.amount - detail.amount,
                is_entry=transaction.is_entry,
                datetime=transaction.datetime,
                method=transaction.method,
            )
        )
        remaining_amount -= detail.amount

    if remaining_amount > 0:
        new_transactions.append(
            TransactionTable(
                note=transaction.note,
                amount=remaining_amount,
                is_entry=transaction.is_entry,
                datetime=transaction.datetime,
                method=transaction.method,
            )
        )
    return new_transactions


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
    categories = session.query(CategoryTable).options(selectinload(CategoryTable.key_texts)).all()
    transactions = IterFunctor(get_transactions(session, from_date, to_date)).map(flat_transaction).reduce(iadd).list()
    transform_ = partial(transform_to_category, transactions)
    results = IterFunctor(categories).map(transform_).list()
    for r in results:
        print(r.total_expenditure())
