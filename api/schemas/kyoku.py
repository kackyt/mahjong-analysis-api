from pydantic import BaseModel, Field
from .generic import GenericList


class Kyoku(BaseModel):
    id: int
    game_id: str
    kyoku_num: int
    honba: int
    reachbou: int
    scores: GenericList[int]
    kazes: GenericList[int]

    class Config:
        orm_mode = True
