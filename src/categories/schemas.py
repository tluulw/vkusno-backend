from src.schemas import CustomBaseModel
from src.types.schemas import TypeWithItemsDTO


class CategoryBase(CustomBaseModel):
    title: str


class CategoryAdd(CategoryBase):
    pass


class CategoryDTO(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class CategoryDelete(CustomBaseModel):
    id: int


class CategoriesWithItemsDTO(CategoryDTO):
    types: list[TypeWithItemsDTO]

    class Config:
        from_attributes = True
