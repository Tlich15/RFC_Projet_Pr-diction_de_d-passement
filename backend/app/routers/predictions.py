from typing import Any, Dict, List
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..services import data_loader

router = APIRouter()


@router.get("/")
def list_predictions() -> JSONResponse:
    rows: List[Dict[str, Any]] = data_loader.get_predictions()
    return JSONResponse(content=jsonable_encoder(rows))