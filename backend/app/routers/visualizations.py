from fastapi import APIRouter

router = APIRouter()


@router.get("/placeholder")
def placeholder() -> dict:
    return {"detail": "Visualization endpoints will be added once data is loaded."}