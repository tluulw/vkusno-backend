from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from src.constants import int_pk
from src.database import Base


class ItemOrm(Base):
    __tablename__ = "item"
    id: Mapped[int_pk]
    title: Mapped[str]
    description: Mapped[str]

    types: Mapped[list["TypeOrm"]] = relationship(
        back_populates="items",
        secondary="item_type"
    )
