from pydantic import BaseModel


class AddTypeToItem(BaseModel):
    item_title: str
    categories_types: list[list]


class AddTypesToItems(BaseModel):
    items: list[AddTypeToItem]
