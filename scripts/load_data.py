import csv
from datetime import datetime

import database as db
from database.models import Transaction

expected_cols = [
    'fecha',
    'hora',
    'transaccion',
    'nota',
    'monto',
]

months = {
    'ene': '01',
    'feb': '02',
    'mar': '03',
    'abr': '04',
    'may': '05',
    'jun': '06',
    'jul': '07',
    'ago': '08',
    'sep': '09',
    'oct': '10',
    'nov': '11',
    'dic': '12',
}


def extract(keys_pos, row):
    return [row[keys_pos[c]] for c in expected_cols]


def to_datetime(date, hour):
    parts = date.split('/')
    month = months[parts[1].lower()]
    return datetime.fromisoformat(f'{parts[2]}-{month}-{parts[0]} {hour}')


def to_orm(keys, row):
    date_, hour, transaction, note, amount_ = extract(keys, row)
    amount = float(amount_)
    return Transaction(
        note=note,
        amount=amount,
        is_entry=amount > 0,
        datetime=to_datetime(date_, hour),
        method=transaction,
    )


def run(data_path):
    with open(data_path) as f:
        data = csv.reader(f)
        columns = list(map(str.lower, next(data)))
        keys = {c: columns.index(c) for c in expected_cols}
        session = db.connect_get_session()
        latest_transaction_datetime = (
            session.query(Transaction.datetime)
            .order_by(Transaction.datetime.desc())
            .first()[0]
        )
        for row in data:


        session.add_all([to_orm(keys, r) for r in data])
        session.commit()
