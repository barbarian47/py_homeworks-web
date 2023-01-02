import pydantic
from typing import Optional


class CreateAdvtSchema(pydantic.BaseModel):
    title: str
    description: str
    author: str

    @pydantic.validator('description')
    def len_advt(cls, value: str):
        if len(value) <= 10:
            raise ValueError('Advertisement is too short')
        return value


class PatchAdvtSchema(pydantic.BaseModel):
    title: Optional[str]
    description: Optional[str]
    author: Optional[str]

    @pydantic.validator('description')
    def len_advt(cls, value: str):
        if len(value) <= 10:
            raise ValueError('Advertisement is too short')
        return value
