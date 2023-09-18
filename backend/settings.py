from functools import lru_cache

from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings


class Settings(
    BaseSettings,
):
    project_name: str
    debug: bool
    database_url: str

    jwt_secret: str
    jwt_algoritm: str
    jwt_expiration: int = 3600
    jwt_reset_jwt_expiration: int = 3600

    mail_username: str
    mail_password: str
    mail_from: str
    mail_from: str

    access_audience: str
    recover_audience: str
    verification_audience: str

    class Config:
        env_prefix = "GAM_"
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
