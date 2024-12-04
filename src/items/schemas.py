from pydantic import BaseModel


class ItemAdd(BaseModel):
    title: str
    image: str
    description: str
    price: int
    size: str


class ListItemAdd(BaseModel):
    items: list[ItemAdd]


class ItemTypeAdd(BaseModel):
    item_id: int
    type_id: int


class ListItemTypeAdd(BaseModel):
    items: list[ItemTypeAdd]
