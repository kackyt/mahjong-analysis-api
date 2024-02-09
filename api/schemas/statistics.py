from pydantic import BaseModel


class AverageScore(BaseModel):
    player_name: str
    score: float
    point: float
    game_count: int

    class Config:
        orm_mode = True


class YakuCount(BaseModel):
    name: str
    han_count: int
    count: int

    class Config:
        orm_mode = True


class NagareCount(BaseModel):
    name: str
    count: int

    class Config:
        orm_mode = True
