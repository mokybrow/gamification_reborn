import datetime
import uuid
from operator import or_
from typing import Any

from pydantic import UUID4, Json
from sqlalchemy import JSON, Text, case, cast, desc, distinct, func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.database_scheme import user_table


async def get_user_img(db: AsyncSession, user_id: UUID4):
    query = select(user_table.c.profile_picture).where(user_table.c.user_id == user_id)
    result = await db.execute(query)
    return result.all()
