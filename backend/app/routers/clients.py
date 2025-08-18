from typing import List
from fastapi import APIRouter, HTTPException, Query

from ..services import data_loader
from ..schemas import ClientRecord

router = APIRouter()


@router.get("/", response_model=List[ClientRecord])
def list_clients() -> List[ClientRecord]:
    clients = data_loader.get_clients()
    return [ClientRecord(**c) for c in clients]


@router.get("/history")
def client_history(client: str = Query(..., description="Client name as it appears in the data")) -> list:
    records = data_loader.get_client_history(client)
    if records is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return records


@router.get("/predictions")
def client_predictions(client: str = Query(..., description="Client name as it appears in the data")) -> list:
    preds = data_loader.get_client_predictions(client)
    if preds is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return preds