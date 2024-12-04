from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.constants import int_pk
from src.database import Base


class ItemOrm(Base):
    __tablename__ = "item"
    id: Mapped[int_pk]
    title: Mapped[str]
    image: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    size: Mapped[str]

    types: Mapped[list["TypeOrm"]] = relationship(
        back_populates="items",
        secondary="item_type"
    )

    def __repr__(self):
        return f"<id: {self.id}, " \
               f"title: {self.title}"


class ItemTypeOrm(Base):
    __tablename__ = "item_type"
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id", ondelete="CASCADE"), primary_key=True)
    type_id: Mapped[int] = mapped_column(ForeignKey("type.id", ondelete="CASCADE"), primary_key=True)
