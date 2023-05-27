import database


def run():
    database.remove_sqlite_db()
    database.create_database()
