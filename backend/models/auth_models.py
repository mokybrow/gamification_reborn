import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr


class BaseUser(BaseModel):
    email: EmailStr
    username: str
    name: Optional[str]
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    gender: Optional[str] = None
    birthdate: Optional[datetime.date] = None
    is_verified: Optional[bool] = False
    is_superuser: Optional[bool] = False
    is_writer: Optional[bool] = False
    registration_date: Optional[datetime.datetime] = None


class UserCreate(BaseUser):
    password: str


class UserUpdate(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    sex: Optional[str] = None
    birthdate: Optional[datetime.date] = None


class UserUpdateImg(BaseModel):
    img: Optional[str] = None


class User(BaseUser):
    user_id: UUID4

    class Config:
        from_attributes = True
        populate_by_name = True


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class VerifyEmail(BaseModel):
    email: EmailStr

class VerifyEmailToken(BaseModel):
    token: str

class ResetPassword(BaseModel):
    token: str
    password: str