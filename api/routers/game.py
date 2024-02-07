from fastapi import APIRouter, Depends, Query
from datetime import date

import api.cruds.game as game_crud
import api.schemas.game as game_schema
from api.auth import verify_token

router = APIRouter()


@router.get("/count", response_model=int)
async def get_games_count(
    dataset_id: str,
    start_date: date,
    end_date: date,
    # _=Depends(verify_token),
):
    return await game_crud.get_games_count(dataset_id, start_date, end_date)


@router.get("", response_model=list[game_schema.Game])
async def get_games(
    dataset_id: str,
    start_date: date,
    end_date: date,
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0),
    # _=Depends(verify_token),
):
    return await game_crud.get_games(dataset_id, start_date, end_date, limit, offset)
