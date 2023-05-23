import database
from database.models import Transaction


def run():
    database.remove_sqlite_db()
    print('Database removed!')
    database.create_database()
    print('Database created!')
