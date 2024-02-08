from fastapi import APIRouter, Depends, Query
import api.cruds.dataset as dataset_cruds
from api.auth import verify_token
from api.schemas.dataset import Dataset

router = APIRouter()


@router.get("", response_model=list[Dataset])
async def get_datasets(
    _=Depends(verify_token),
):
    return await dataset_cruds.get_datasets()
