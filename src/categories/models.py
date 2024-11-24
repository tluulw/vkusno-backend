from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.constants import int_pk
from src.database import Base


class CategoryOrm(Base):
    __tablename__ = 'category'
    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(unique=True)

    types: Mapped[list["TypeOrm"]] = relationship(
        back_populates="category"
    )
