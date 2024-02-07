from fastapi import APIRouter, Depends, Query
from datetime import date

import api.cruds.statstics as statistics_crud
import api.schemas.statistics as statistics_schema
from api.auth import verify_token

router = APIRouter()


@router.get("/average_score_by_player", response_model=list[statistics_schema.AverageScore])
async def get_average_score_by_player(
    dataset_id: str,
    start_date: date,
    end_date: date,
    # _=Depends(verify_token),
):
    return await statistics_crud.get_average_score_by_player(dataset_id, start_date, end_date)


@router.get("/yaku_count", response_model=list[statistics_schema.YakuCount])
async def get_yaku_count(
    dataset_id: str,
    start_date: date,
    end_date: date,
    # _=Depends(verify_token),
):
    return await statistics_crud.get_yaku_count(dataset_id, start_date, end_date)


@router.get("/nagare_count", response_model=list[statistics_schema.NagareCount])
async def get_nagare_count(
    dataset_id: str,
    start_date: date,
    end_date: date,
    # _=Depends(verify_token),
):
    return await statistics_crud.get_nagare_count(dataset_id, start_date, end_date)
