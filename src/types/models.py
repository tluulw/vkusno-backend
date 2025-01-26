from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.constants import int_pk
from src.database import Base


class TypeOrm(Base):
    __tablename__ = "type"
    id: Mapped[int_pk]
    title: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id", ondelete="CASCADE", onupdate="CASCADE"))

    category: Mapped["CategoryOrm"] = relationship(back_populates="types")

    items: Mapped[list["ItemOrm"]] = relationship(
        back_populates="types",
        secondary="item_type"
    )
