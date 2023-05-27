import operator
import struct
from functools import partial, reduce
from operator import itemgetter

import database
from core.functors import IterFunctor
from core.utils import split_keywords
from database.models import TransactionTable, CategoryTable


def get_key(t: TransactionTable):
    return str(t.note).lower().strip()


def is_not_categorized(categories_keywords: list, note: str) -> bool:
    for c in categories_keywords:
        if c in note:
            return False
    return True


def run():
    session = database.connect_get_session()
    transactions = session.query(TransactionTable).filter(TransactionTable.is_entry.is_(False))

    categories_query = session.query(CategoryTable.keywords).filter(CategoryTable.keywords != "").all()
    keywords = (
        IterFunctor(categories_query)
        .map(itemgetter(0))
        .map(split_keywords)
        .apply(partial(reduce, operator.iadd))
        .list()
    )

    _is_not = partial(is_not_categorized, keywords)
    result = set(filter(_is_not, map(get_key, transactions)))
    for r in result:
        print(r)
