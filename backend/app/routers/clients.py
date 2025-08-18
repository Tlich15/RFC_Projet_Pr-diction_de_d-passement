from typing import List
from fastapi import APIRouter

from ..services import data_loader
from ..schemas import ClientRecord

router = APIRouter()


@router.get("/", response_model=List[ClientRecord])
def list_clients() -> List[ClientRecord]:
    clients = data_loader.get_clients()
    return [ClientRecord(**c) for c in clients]