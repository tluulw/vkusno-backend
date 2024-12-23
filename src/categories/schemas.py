from pydantic import BaseModel


class CategoryAdd(BaseModel):
    title: str


class ListCategoryAdd(BaseModel):
    categories: list[CategoryAdd]


class CategoryShow(BaseModel):
    id: int
    title: str


class ListCategoryShow(BaseModel):
    categories: list[CategoryShow]
