from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime

from database import Base


class TransactionTable(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    note = Column(String(128), nullable=False)
    amount = Column(Numeric(2), nullable=False)
    is_entry = Column(Boolean, nullable=False)
    datetime = Column(DateTime, nullable=False)
    method = Column(String(128), nullable=False)

    def __repr__(self):
        return f'{self.amount=} {self.note=} {self.is_entry=} {self.datetime=} {self.method=}'


class CategoryTable(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    keywords = Column(String(256), nullable=False)
