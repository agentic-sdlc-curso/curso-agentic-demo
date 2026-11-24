"""Application factory and entry point (uvicorn app.main:app)."""

from fastapi import FastAPI

from app.errors import ServiceRequestsAPI, register_error_handlers
from app.requests.routes import router as requests_router


def create_app() -> FastAPI:
    app = ServiceRequestsAPI(title="Service Requests API")
    register_error_handlers(app)
    app.include_router(requests_router)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
