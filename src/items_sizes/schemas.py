from src.schemas import CustomBaseModel


class ItemSizeBase(CustomBaseModel):
    item_id: int
    image: str
    price: int
    size: str


class ItemSizeAdd(ItemSizeBase):
    pass


class ItemSizeDTO(ItemSizeBase):
    pass

    class Config:
        from_attributes = True


class ItemSizeDelete(CustomBaseModel):
    item_id: int
    size: str
