
import uuid
from pydantic import UUID4
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.database_scheme import game_table, platforms, genres, age_rating_games, game_genres, game_platforms, age_ratings
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
    offset = 30400
    end_of_base = True
    while end_of_base:
        query = (select(
                        game_table
                        )
                        .offset(offset)
                        .limit(1)
                        .where(game_table.c.esrb_rating != None)
                    )
        result = await db.execute(query)
        result = result.all()
        # print(result)
        # print(result[0][16])
        if result:
            if result[0][16]:

                query_id = select(age_ratings.c.age_rating_id).where(age_ratings.c.name==result[0][16])
                query_id = await db.execute(query_id)
                query_id = query_id.all()

                # print(query_id[0][0])
                # print(result[0][0])

                check_pair = select(age_rating_games).where(age_rating_games.c.game_id==result[0][0],
                                    age_rating_games.c.age_rating_id==query_id[0][0])
                check_pair = await db.execute(check_pair)
                check_pair = check_pair.all()
                if not check_pair:
                    stmt = insert(age_rating_games).values(
                                        game_id=result[0][0],
                                        age_rating_id=query_id[0][0]
                                    )

                    await db.execute(stmt)
                    await db.commit()
                offset+=1

                print(offset)
        else:
            end_of_base = False
