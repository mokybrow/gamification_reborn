from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.auth_models import User, UserUpdate, UserUpdateImg
from api.schemas.database import user_table


class AuthUtils:
    @staticmethod
    async def get_user_by_email(email: str, db: AsyncSession):
        query = select(user_table).where(
            func.lower(user_table.c.email) == email.lower(),
        )
        result = await db.execute(query)
        return result.all()

    @staticmethod
    async def get_user_by_username(username: str, db: AsyncSession):
        query = select(user_table).where(
            func.lower(user_table.c.username) == username.lower(),
        )
        result = await db.execute(query)
        return result.all()

    async def is_verified(self, user: User) -> bool:
        return user.is_verified

    async def verify_user_by_email(self, email: str, db: AsyncSession) -> bool:
        stmt = update(user_table).where(user_table.c.email == email).values(is_verified=True)
        await db.execute(stmt)
        await db.commit()

    async def add_new_password(self, email: str, new_password: str, db: AsyncSession):
        stmt = update(user_table).where(user_table.c.email == email).values(hashed_password=new_password)
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
        self,
        email: str,
        user: UserUpdateImg,
        db: AsyncSession,
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
