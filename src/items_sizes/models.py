from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class ItemSizeOrm(Base):
    __tablename__ = "item_size"
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id", ondelete="CASCADE"), primary_key=True)
    image: Mapped[str]
    price: Mapped[int]
    size: Mapped[str] = mapped_column(primary_key=True)

    item: Mapped["ItemOrm"] = relationship(
        back_populates="sizes"
    )
