from pydantic import BaseModel


class TypeAdd(BaseModel):
    title: str = 'default'  # default is for categories with 1 type
    category_id: int


class ListTypeAdd(BaseModel):
    types: list[TypeAdd]
