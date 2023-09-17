import datetime
from typing import Optional

from pydantic import UUID4, BaseModel


class BaseUser(BaseModel):
    email: str
    username: str
    name: Optional[str] = None
    surname: Optional[str] = None
    img: Optional[str] = None
    sex: Optional[str] = None
    birthdate: Optional[datetime.date] = None
    is_verified: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_writer: Optional[bool] = None


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    id: UUID4

    class Config:
        from_attributes = True
        populate_by_name = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ResetUser(BaseModel):
    id: UUID4
    email: str
    username: str
    hashed_password: str
