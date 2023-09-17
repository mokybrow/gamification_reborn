from functools import lru_cache

from fastapi import APIRouter, FastAPI

from backend.transport.auth import router as test_router

from .settings import get_settings


def _setup_api_routers(
    api: APIRouter,
) -> None:
    api.include_router(test_router)


@lru_cache
def make_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.project_name,
        # debug=settings.debug,
    )
    _setup_api_routers(app.router)  # noqa

    return app
