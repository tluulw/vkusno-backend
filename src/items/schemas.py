from src.schemas import CustomBaseModel


class ItemBase(CustomBaseModel):
    title: str
    description: str


class ItemAdd(ItemBase):
    pass


class ItemDTO(ItemBase):
    id: int

    class Config:
        from_attributes = True


class ItemDelete(CustomBaseModel):
    id: int
