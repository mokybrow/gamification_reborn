from ast import Dict
from typing import Any, Optional

from fastapi import Depends
from jose import JWTError
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_async_session
from backend.models.auth import ResetUser
from backend.models.database import user_table
from backend.settings import get_settings

settings = get_settings()


class AuthUtils:
    async def get_user_by_email(
        self, db: AsyncSession, *, email: str
    ) -> Optional[ResetUser]:
        user = await db.execute(select(user_table).filter(user_table.c.email == email))
        user = user.all()
        for row in user:
            user = row._mapping
        return user
    
    async def update_user_password(
        self, db: AsyncSession, *, password: str, email:str
    ):
        user = await db.execute(update(user_table).where(user_table.c.email == email).values(hashed_password = password))
        await db.commit()
        return user

    async def update_user_data(
            self, db: AsyncSession, *, password: str, email:str
    ):
        pass