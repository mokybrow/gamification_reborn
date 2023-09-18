import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr


class BaseUser(BaseModel):
    email: EmailStr
    username: str
    name: Optional[str] = None
    surname: Optional[str] = None
    img: Optional[str] = None
    sex: Optional[str] = None
    birthdate: Optional[datetime.date] = None
    is_verified: Optional[bool] = False
    is_superuser: Optional[bool] = False
    is_writer: Optional[bool] = False


class UserCreate(BaseUser):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    sex: Optional[str] = None
    birthdate: Optional[datetime.date] = None


class UserUpdateImg(BaseModel):
    img: Optional[str] = None


class User(BaseUser):
    id: UUID4

    class Config:
        from_attributes = True
        populate_by_name = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
