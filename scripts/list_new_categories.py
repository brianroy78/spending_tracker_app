import operator
from functools import partial, reduce
from operator import itemgetter

import database
from core.functors import IterFunctor
from database.models import TransactionTable, KeyTextTable


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

    categories_query = session.query(KeyTextTable.text).all()
    key_texts = IterFunctor(categories_query).map(itemgetter(0)).list()
    _is_not = partial(is_not_categorized, key_texts)
    result = set(filter(_is_not, map(get_key, transactions)))
    for r in result:
        print(r)
