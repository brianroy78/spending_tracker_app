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


def run(data_path):
    with open(data_path) as f:
        data = csv.reader(f)
        columns = list(map(str.lower, next(data)))
        keys = {c: columns.index(c) for c in expected_cols}
        session = db.connect_get_session()
        result = session.query(TransactionTable.datetime).order_by(TransactionTable.datetime.desc()).first()
        latest_transaction_datetime = result[0] if result is not None else None
        for row in data:
            date_, hour, transaction, note, amount_ = extract(keys, row)
            datetime_ = to_datetime(date_, hour)
            if latest_transaction_datetime is not None and datetime_ <= latest_transaction_datetime:
                break
            amount = float(amount_)
            session.add(
                TransactionTable(
                    note=note,
                    amount=amount,
                    is_entry=amount > 0,
                    datetime=to_datetime(date_, hour),
                    method=transaction,
                )
            )

        session.commit()
