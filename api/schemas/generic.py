from pydantic import BaseModel
from typing import TypeVar, Generic

T = TypeVar("T")


class Element(BaseModel, Generic[T]):
    element: T

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class GenericList(BaseModel, Generic[T]):
    list: list[Element[T]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
