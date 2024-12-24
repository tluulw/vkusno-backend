from src.schemas import CustomBaseModel


class TypeBase(CustomBaseModel):
    title: str = 'default'  # default is for categories with 1 type
    category_id: int


class TypeAdd(TypeBase):
    pass


class TypeDTO(TypeBase):
    id: int

    class Config:
        from_attributes = True


class TypeDelete(CustomBaseModel):
    id: int
