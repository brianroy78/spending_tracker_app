from datetime import datetime, timedelta
from functools import partial
from operator import attrgetter, is_not
from typing import Optional

from sqlalchemy.orm import selectinload

import database as db
from core.functors import IterFunctor
from core.models import Category, Transaction
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


def flat_transaction(transaction: TransactionTable) -> Optional[TransactionTable]:
    if is_empty(transaction.details):
        return transaction
    new_amount = transaction.amount - sum([d.amount for d in transaction.details])
    if new_amount <= 0:
        return None
    return TransactionTable(
        id=transaction.id,
        note=transaction.note,
        amount=new_amount,
        is_entry=transaction.is_entry,
        datetime=transaction.datetime,
        method=transaction.method,
    )


def detail_to_transaction(detail: TransactionDetailTable) -> Transaction:
    return Transaction(
        note=detail.transaction.note,
        amount=detail.amount,
        is_entry=detail.transaction.is_entry,
        datetime=detail.transaction.datetime,
        method=detail.transaction.method,
    )


def transform_to_category(transactions: list[TransactionTable], category: CategoryTable) -> Category:
    key_texts = IterFunctor(category.key_texts).map(attrgetter("text")).list()
    filter_ = partial(match, key_texts)
    defined = [detail_to_transaction(d) for d in category.details]
    matched_transactions = IterFunctor(transactions).filter(filter_).list()
    return Category(
        name=category.name,
        key_texts=key_texts,
        transactions=matched_transactions + defined,
    )


def run(from_: str, to: str):
    from_date = datetime.fromisoformat(from_)
    to_date = datetime.fromisoformat(to)
    session = db.connect_get_session()
    categories = (
        session.query(CategoryTable)
        .options(selectinload(CategoryTable.key_texts), selectinload(CategoryTable.details))
        .all()
    )
    is_not_none = partial(is_not, None)
    transactions = (
        IterFunctor(get_transactions(session, from_date, to_date)).map(flat_transaction).filter(is_not_none).list()
    )
    transform_ = partial(transform_to_category, transactions)
    results = IterFunctor(categories).map(transform_).list()
    for r in results:
        print(r.total_expenditure())
