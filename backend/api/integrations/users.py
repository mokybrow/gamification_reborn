import datetime

from pydantic import UUID4
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.database import user_table


async def change_user_data(id: UUID4, name: str, bio: str, birthdate: datetime.date, db: AsyncSession):
    try:
        stmt = update(user_table).values(name=name, bio=bio, birthdate=birthdate).where(user_table.c.id == id)
        await db.execute(stmt)
        await db.commit()
        return True
    except:
        return False
