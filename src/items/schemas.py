from pydantic import BaseModel


class ItemAdd(BaseModel):
    title: str
    image: str
    description: str
    price: int
    size: str


class ListItemAdd(BaseModel):
    items: list[ItemAdd]
