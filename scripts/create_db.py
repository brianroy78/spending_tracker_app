import database
from core.models import ExpenditureCategories
from database.models import TransactionTable, CategoryTable

essentials = ["hipermaxi", "fidalga"]
eating_outs = ["polloskiky", "lafabricadebiancaflor", "tortasdolly", "frida"]
healths = ["farmacia", "hospital", "farmacorp"]
car = ["surtidor", "combustible"]


def run():
    database.remove_sqlite_db()
    database.create_database()
    session = database.connect_get_session()
    session.add(CategoryTable(name=ExpenditureCategories.ESSENTIALS.value, keywords="|".join(essentials)))
    session.add(CategoryTable(name=ExpenditureCategories.EATING_OUT.value, keywords="|".join(eating_outs)))
    session.add(CategoryTable(name=ExpenditureCategories.ENTERTAINMENT.value, keywords=""))
    session.add(CategoryTable(name=ExpenditureCategories.HEALTH.value, keywords="|".join(healths)))
    session.add(CategoryTable(name=ExpenditureCategories.CAR.value, keywords="|".join(car)))
    session.add(CategoryTable(name=ExpenditureCategories.GIFTS.value, keywords=""))
    session.add(CategoryTable(name=ExpenditureCategories.CLOTHES.value, keywords=""))
    session.add(CategoryTable(name=ExpenditureCategories.UNKNOWN.value, keywords=""))
    session.commit()
