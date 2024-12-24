from pydantic import BaseModel


class CustomBaseModel(BaseModel):
    @classmethod
    def from_orm_to_json(cls, orm_obj):
        return cls.model_validate(orm_obj).model_dump()
