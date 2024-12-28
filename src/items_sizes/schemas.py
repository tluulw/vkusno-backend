from src.schemas import CustomBaseModel


class ItemSizeBase(CustomBaseModel):
    image: str
    price: int
    size: str


class ItemSizeAdd(ItemSizeBase):
    item_id: int


class ItemSizeDTO(ItemSizeAdd):
    pass

    class Config:
        from_attributes = True


class ItemSizeDelete(CustomBaseModel):
    item_id: int
    size: str
