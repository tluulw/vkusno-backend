from sqlalchemy.orm import Mapped

from src.database import Base
from src.constants import int_pk


class ItemOrm(Base):
    __tablename__ = 'item'
    id: Mapped[int_pk]
    title: Mapped[str]
    image: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    size: Mapped[str]

    def __repr__(self):
        return f"<id: {self.id}, "\
               f"title: {self.title}, "\
               f"image: {self.image}, "\
               f"description: {self.description}, "\
               f"price: {self.price}, "\
               f"size: {self.size}>"
