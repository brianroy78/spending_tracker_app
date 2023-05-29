from datetime import datetime, timedelta
from functools import partial
from operator import attrgetter

import database as db
from core import utils
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


def run(from_: str, to: str):
    from_date = datetime.fromisoformat(from_)
    to_date = datetime.fromisoformat(to)
    session = db.connect_get_session()
    categories = session.query(CategoryTable).all()
    results = []
    transactions = get_transactions(session, from_date, to_date)
    for c in categories:
        key_texts = IterFunctor(c.key_texts).map(attrgetter("text")).list()
        filter_ = partial(match, key_texts)
        results.append(
            Category(
                name=c.name,
                key_texts=key_texts,
                transactions=IterFunctor(transactions).filter(filter_).list(),
            )
        )

    for r in results:
        print(r.total_expenditure())
