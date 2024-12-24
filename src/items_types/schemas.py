from src.schemas import CustomBaseModel


class ItemTypeBase(CustomBaseModel):
    item_id: int
    type_id: int


class ItemTypeAdd(ItemTypeBase):
    pass


class ItemTypeDTO(ItemTypeBase):
    pass

    class Config:
        from_attributes = True


class ItemTypesDelete(CustomBaseModel):
    item_id: int


class ItemTypeDelete(ItemTypesDelete):
    type_id: int
