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
    text: Mapped[str] = mapped_column(String(128))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
