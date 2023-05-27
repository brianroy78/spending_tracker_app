import database
from database.models import CategoryTable


def run():
    session = database.connect_get_session()
    session.add(CategoryTable())
    session.commit()
