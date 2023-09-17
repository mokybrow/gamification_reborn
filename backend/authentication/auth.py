import datetime
import json
import uuid
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_async_session
from backend.models.auth import Token, User, UserCreate
from backend.models.database import user_table
from backend.settings import get_settings

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign-in")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return await AuthService.validate_token(token)


class AuthService:
    @classmethod
    async def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    async def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    async def validate_token(cls, token: str) -> User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not valid creditials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                audience=settings.access_audience,
                algorithms=settings.jwt_algoritm,
            )
        except JWTError:
            raise exception from None

        user_data = payload.get("user")
        user_data = json.loads(user_data)

        try:
            user = User.model_validate(user_data)

        except ValidationError:
            raise exception from None
        return user

    @classmethod
    async def create_access_token(cls, user: UserCreate) -> Token:
        user_data = User(**user)
        now = datetime.datetime.utcnow()
        payload = {
            "iat": now,
            "nbf": now,
            "exp": now + datetime.timedelta(seconds=settings.jwt_expiration),
            "sub": str(user_data.id),
            "aud": settings.access_audience,
            "user": user_data.model_dump_json(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algoritm,
        )
        return Token(access_token=token)

    @classmethod
    async def create_recover_token(cls, user: UserCreate) -> Token:
        user_data = User(**user)
        now = datetime.datetime.utcnow()
        payload = {
            "iat": now,
            "nbf": now,
            "exp": now + datetime.timedelta(seconds=settings.jwt_expiration),
            "sub": str(user_data.id),
            "aud": settings.recover_audience,
            "user": user_data.model_dump_json(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algoritm,
        )
        print(token)
        return Token(access_token=token)

    def __init__(self, db: AsyncSession = Depends(get_async_session)):
        self.db = db

    async def registration_user(self, user_data: UserCreate) -> Token:
        user = {
            "id": uuid.uuid4(),
            "email": user_data.email,
            "username": user_data.username,
            "name": user_data.name,
            "surname": user_data.surname,
            "img": user_data.img,
            "sex": user_data.sex,
            "birthdate": user_data.birthdate,
            "is_verified": user_data.is_verified,
            "is_superuser": user_data.is_superuser,
            "is_writer": user_data.is_writer,
            "hashed_password": await self.hash_password(user_data.password),
        }
        await self.db.execute(insert(user_table).values(user))

        await self.db.commit()

        return await self.create_access_token(user)

    async def authenticate_user(self, username: str, password: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not valid creditials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        user = await self.db.execute(
            select(user_table).filter(user_table.c.username == username)
        )
        user = user.all()
        for row in user:
            user = row._mapping
        if not user:
            raise exception

        if not await self.verify_password(password, user.hashed_password):
            raise exception

        return await self.create_access_token(user)

    async def recover_password(self, email: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't find user",
            headers={"WWW-Authenticate": "Bearer"},
        )
        user = await self.db.execute(
            select(user_table).filter(user_table.c.email == email)
        )
        user = user.all()
        for row in user:
            user = row._mapping
        if not user:
            raise exception
        
        return await self.create_recover_token(user)

    async def validate_recover_token(self, token: str) -> bool:
        exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                audience=settings.recover_audience,
                algorithms=settings.jwt_algoritm,
            )
        except JWTError:
            raise exception from None

        user_data = payload.get("user")
        user_data = json.loads(user_data)

        try:
            user = User.model_validate(user_data)

        except ValidationError:
            raise exception from None
        
        return True
