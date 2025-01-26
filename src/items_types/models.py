from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class ItemTypeOrm(Base):
    __tablename__ = "item_type"
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id", ondelete="CASCADE", onupdate="CASCADE"),
                                         primary_key=True)
    type_id: Mapped[int] = mapped_column(ForeignKey("type.id", ondelete="CASCADE", onupdate="CASCADE"),
                                         primary_key=True)
