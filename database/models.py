from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime

from database import Base


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    note = Column(String(128), nullable=False)
    amount = Column(Numeric(2), nullable=False)
    is_entry = Column(Boolean, nullable=False)
    datetime = Column(DateTime, nullable=False)
    method = Column(String(128), nullable=False)
