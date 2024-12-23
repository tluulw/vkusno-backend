from pydantic import BaseModel


class ItemAdd(BaseModel):
    title: str


class ItemSizeAdd(BaseModel):
    item_id: int
    title: str
    image: str
    description: str
    price: int
    size: str


class ListItemAdd(BaseModel):
    items: list[ItemAdd]


class ListItemSizeAdd(BaseModel):
    items: list[ItemSizeAdd]


class ItemTypeAdd(BaseModel):
    item_id: int
    type_id: int


class ListItemTypeAdd(BaseModel):
    items: list[ItemTypeAdd]


class ItemShow(BaseModel):
    id: int
    title: str
