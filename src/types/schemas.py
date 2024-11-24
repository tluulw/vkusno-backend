from pydantic import BaseModel


class TypeAdd(BaseModel):
    title: str
    category_id: int


class ListTypeAdd(BaseModel):
    types: list[TypeAdd]
