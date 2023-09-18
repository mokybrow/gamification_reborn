import json

from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.auth import (Token, User, UserCreate, UserUpdate,
                                 UserUpdateImg)
from backend.models.database import user_table


class AuthUtils:

    @staticmethod
    async def get_user_by_email( email: str, db: AsyncSession):
        query = select(user_table).where(user_table.c.email == email)
        result = await db.execute(query)
        return result.all()
    
    @staticmethod
    async def get_user_by_username( username: str, db: AsyncSession):
        query = select(user_table).where(user_table.c.username == username)
        result = await db.execute(query)
        return result.all()

    async def is_verified(self, user: User) -> bool:
        return user.is_verified

    async def verify_user_by_email(self, email: str, db: AsyncSession) -> bool:
        stmt = (
            update(user_table)
            .where(user_table.c.email == email)
            .values(is_verified=True)
        )
        await db.execute(stmt)
        await db.commit()

    async def add_new_password(self, email: str, new_password: str, db: AsyncSession):
        stmt = (
            update(user_table)
            .where(user_table.c.email == email)
            .values(hashed_password=new_password)
        )
        await db.execute(stmt)
        await db.commit()
        # return result.all()

    async def update_user_data(self, email: str, user: UserUpdate, db: AsyncSession):
        stmt = (
            update(user_table)
            .where(user_table.c.email == email)
            .values(
                name=user.name,
                surname=user.surname,
                sex=user.sex,
                birthdate=user.birthdate,
            )
        )
        await db.execute(stmt)
        await db.commit()
        return True

    async def update_user_image(
        self, email: str, user: UserUpdateImg, db: AsyncSession
    ):
        stmt = (
            update(user_table)
            .where(user_table.c.email == email)
            .values(
                img=user.img,
            )
        )
        await db.execute(stmt)
        await db.commit()
        return True
