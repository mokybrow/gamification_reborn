from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.database import user_table, profile_pictures


async def get_user_img(db: AsyncSession, id: UUID4):
    query = select(profile_pictures.c.og_picture_path).where(profile_pictures.c.user_id == id)
    result = await db.execute(query)
    return result.all()
