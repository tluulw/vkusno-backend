from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.constants import int_pk


class CategoryOrm(Base):
    __tablename__ = 'category'
    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(unique=True)


class TypeOrm(Base):
    __tablename__ = 'type'
    id: Mapped[int_pk]
    title: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id", ondelete="CASCADE"))
