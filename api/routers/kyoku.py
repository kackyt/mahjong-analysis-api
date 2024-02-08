from fastapi import APIRouter, Depends, Query
from datetime import date

import api.cruds.kyoku as kyoku_crud
import api.schemas.kyoku as kyoku_schema
from api.auth import verify_token

router = APIRouter()


@router.get("/count", response_model=int)
async def get_kyokus_count(
    dataset_id: str,
    start_date: date,
    end_date: date,
    game_id: str | None = None,
    _=Depends(verify_token),
):
    return await kyoku_crud.get_kyokus_count(dataset_id, start_date, end_date, game_id)


@router.get("", response_model=list[kyoku_schema.Kyoku])
async def get_kyokus(
    dataset_id: str,
    start_date: date,
    end_date: date,
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0),
    game_id: str | None = None,
    _=Depends(verify_token),
):
    return await kyoku_crud.get_kyokus(dataset_id, start_date, end_date, limit, offset, game_id)
