from typing import Any, Dict, List
from fastapi import APIRouter

from ..services import data_loader

router = APIRouter()


@router.get("/", response_model=List[Dict[str, Any]])
def list_predictions() -> List[Dict[str, Any]]:
    return data_loader.get_predictions()