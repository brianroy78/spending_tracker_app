from datetime import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base


class TransactionTable(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(primary_key=True)
    note: Mapped[str] = mapped_column(String(128))
    amount: Mapped[int]
    is_entry: Mapped[bool]
    datetime: Mapped[datetime]
    method: Mapped[str] = mapped_column(String(128), nullable=False)
    details: Mapped[list["TransactionDetailTable"]] = relationship("TransactionDetailTable")

    def __repr__(self):
        return f"{self.amount=} {self.note=} {self.is_entry=} {self.datetime=} {self.method=}"


class CategoryTable(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    key_texts: Mapped[list["KeyTextTable"]] = relationship("KeyTextTable")


class KeyTextTable(Base):
    __tablename__ = "key_text"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(128), unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))


class TransactionDetailTable(Base):
    __tablename__ = "transaction_detail"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int]
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    transaction_id: Mapped[int] = mapped_column(ForeignKey("transaction.id"))
    category: Mapped["CategoryTable"] = relationship("CategoryTable")
