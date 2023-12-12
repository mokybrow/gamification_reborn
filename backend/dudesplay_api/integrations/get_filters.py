
import uuid
from pydantic import UUID4
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.database_scheme import game_table, platforms, g_tags, genres, age_rating_games
from deep_translator import GoogleTranslator, MyMemoryTranslator


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


async def normilize(db: AsyncSession):
    offset = 158000
    end_of_base = True
    while end_of_base:
        query = (select(
                        game_table
                        )
                        .offset(offset)
                        .limit(1)
                    )
        result = await db.execute(query)
        result = result.all()
        # print(result[0][11]) # тэги
        if result:
            # print(result[0][11])
            if result[0][11]:
                for tag in result[0][11]:
                    query = (select(
                                g_tags
                                ).where(g_tags.c.name==tag)
                            )
                    tag_query = await db.execute(query)
                    tag_query = tag_query.all()
                    if not tag_query:
                        stmt = insert(g_tags).values(
                                g_tag_id=uuid.uuid4(),
                                name=tag
                            )

                        await db.execute(stmt)
                        await db.commit()
                # print(result[0][10]) # жанры
            # print(result[0][10])
            if result[0][10]:
                for genre in result[0][10]:
                    query = (select(
                                genres
                                ).where(genres.c.name==genre)
                            )
                    genre_query = await db.execute(query)
                    genre_query = genre_query.all()
                    if not genre_query:
                        stmt = insert(genres).values(
                                genre_id=uuid.uuid4(),
                                name=genre
                            )

                        await db.execute(stmt)
                        await db.commit()

        # print(result[0][9]) # parent_platform

        # print(result[0][8]) # platform_name
        # print(result[0][7]) # platform_slug

        offset+=1
