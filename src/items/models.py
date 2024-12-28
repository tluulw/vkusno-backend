from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from src.constants import int_pk
from src.database import Base


class ItemOrm(Base):
    __tablename__ = "item"
    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]

    types: Mapped[list["TypeOrm"]] = relationship(
        back_populates="items",
        secondary="item_type"
    )

    sizes: Mapped[list["ItemSizeOrm"]] = relationship(
        back_populates="item",
        cascade='all, delete'
    )
