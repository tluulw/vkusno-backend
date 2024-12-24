from src.schemas import CustomBaseModel


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
