from pydantic import BaseModel


class CategoryAdd(BaseModel):
    title: str


class ListCategoryAdd(BaseModel):
    categories: list[CategoryAdd]
