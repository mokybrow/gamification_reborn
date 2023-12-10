
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.database_scheme import game_table


async def get_filters_bd(db: AsyncSession, genre: str | None = None, platform: str | None = None):
    qs = []
    if genre is not None:
        qs.append(game_table.c.genre.any(genre))
        # query = select(game_table.c.title).where(game_table.c.genre.any(genre)).limit(20)

    if platform is not None:
        qs.append(game_table.c.platform_slug.any(platform))
        # query = select(game_table.c.title).where(game_table.c.platforms.any(platform)).limit(20)
    query = select(game_table.c.title).filter(*qs).limit(20)
    result = await db.execute(query)
    result = result.all()
    return result
