from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routers.data import router as data_router
from .routers.clients import router as clients_router
from .routers.predictions import router as predictions_router
from .routers.visualizations import router as visualizations_router


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="Monthly Exceedance Prediction API", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(data_router, prefix="/data", tags=["data"])
    app.include_router(clients_router, prefix="/clients", tags=["clients"])
    app.include_router(predictions_router, prefix="/predictions", tags=["predictions"])
    app.include_router(visualizations_router, prefix="/visualizations", tags=["visualizations"])
    return app


app = create_app()