from pydantic import BaseModel, Field


class Dataset(BaseModel):
    id: str
    friendly_name: str | None

    class Config:
        orm_mode = True
