from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.database import profile_pictures, user_table


async def get_user_img(db: AsyncSession, id: UUID4):
    query = select(profile_pictures.c.og_picture_path).where(profile_pictures.c.user_id == id)
    result = await db.execute(query)
    return result.all()
