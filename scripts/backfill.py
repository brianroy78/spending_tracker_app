import csv
from datetime import datetime

import database as db
from database.models import TransactionTable

expected_cols = [
    "fecha",
    "hora",
    "transaccion",
    "nota",
    "monto",
]

months = {
    "ene": "01",
    "feb": "02",
    "mar": "03",
    "abr": "04",
    "may": "05",
    "jun": "06",
    "jul": "07",
    "ago": "08",
    "sep": "09",
    "oct": "10",
    "nov": "11",
    "dic": "12",
}


def extract(keys_pos, row):
    return [row[keys_pos[c]] for c in expected_cols]


def to_datetime(date, hour):
    parts = date.split("/")
    month = months[parts[1].lower()]
    return datetime.fromisoformat(f"{parts[2]}-{month}-{parts[0]} {hour}")


def get_transactions_dict(session):
    return {
        (
            t.note,
            t.datetime,
        ): t
        for t in session.query(TransactionTable)
    }


def run(data_path):
    with open(data_path) as f:
        data = csv.reader(f)
        columns = list(map(str.lower, next(data)))
        keys = {c: columns.index(c) for c in expected_cols}
        session = db.connect_get_session()
        t_dict = get_transactions_dict(session)
        counter = 0
        for row in data:
            date_, hour, transaction, note, amount_ = extract(keys, row)
            datetime_ = to_datetime(date_, hour)
            counter += 1
            amount = int(float(amount_) * 100)
            t = t_dict[(note, datetime_)]
            t.amount = amount

        session.commit()
        print(f"{counter} new Transactions inserted!")
