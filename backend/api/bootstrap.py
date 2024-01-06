from functools import lru_cache

from fastapi import APIRouter, FastAPI

from api.transport.auth_router import router as auth_router
from api.transport.experemental import router as exp
from api.transport.user_router import router as user_router

from .settings import get_settings


def _setup_api_routers(
    api: APIRouter,
) -> None:
    api.include_router(auth_router)
    api.include_router(user_router)
    api.include_router(exp)


@lru_cache
def make_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.project_name,
        # debug=settings.debug,
    )
    _setup_api_routers(app.router)

    return app
