from src.items_sizes.schemas import ItemSizeBase, ItemSizeDTO
from src.schemas import CustomBaseModel


class ItemBase(CustomBaseModel):
    title: str
    description: str


class ItemAdd(ItemBase):
    pass


class ItemWithSizeAdd(ItemAdd):
    sizes: list[ItemSizeBase]


class ItemDTO(ItemBase):
    id: int
    sizes: list[ItemSizeDTO]

    class Config:
        from_attributes = True


class ItemDelete(CustomBaseModel):
    id: int
