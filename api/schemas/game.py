from pydantic import BaseModel, Field
from datetime import datetime


class Game(BaseModel):
    id: str
    title: str = Field(default="Mahjong")
    tonpu: bool
    ariari: bool
    has_aka: bool
    demo: bool
    soku: bool
    level: int
    started_at: datetime

    class Config:
        orm_mode = True
