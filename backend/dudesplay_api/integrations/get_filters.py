
import uuid
from pydantic import UUID4
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.database_scheme import game_table, platforms, g_tags, genres, age_rating_games, game_tags, game_genres, game_platforms
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
    offset = 461400
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
        # print(result)
        # print(result[0][11]) # тэги
        # print(result[0][0])
        if result:
            if result[0][7]:
                for platform_slug in result[0][7]:
                    platform_id = select(platforms).where(platforms.c.platform_slug == platform_slug)
                    platform_id = await db.execute(platform_id)
                    platform_id = platform_id.all()

                    check_pair = select(game_platforms).filter(game_platforms.c.game_id == result[0][0], game_platforms.c.platform_id == platform_id[0][0] )
                    check_pair = await db.execute(check_pair)
                    check_pair = check_pair.all()
                    if not check_pair:
                        stmt = insert(game_platforms).values(
                                game_id=result[0][0],
                                platform_id=platform_id[0][0]
                                )

                        await db.execute(stmt)
                        await db.commit()
            if result[0][10]:
                for game_genre in result[0][10]:
                    game_genre_id = select(genres).where(genres.c.name == game_genre)
                    game_genre_id = await db.execute(game_genre_id)
                    game_genre_id = game_genre_id.all()
           
                    check_pair2 = select(game_genres).filter(game_genres.c.game_id == result[0][0], game_genres.c.genre_id == game_genre_id[0][0])
                    check_pair2 = await db.execute(check_pair2)
                    check_pair2 = check_pair2.all()
                    if not check_pair2:

                        stmt = insert(game_genres).values(
                                game_id=result[0][0],
                                genre_id=game_genre_id[0][0]
                                )

                        await db.execute(stmt)
                        await db.commit()               
            # print(result[0][11])
            # if result[0][11]:
            #     for tag in result[0][11]:
            #         query = (select(
            #                     g_tags
            #                     ).where(g_tags.c.name==tag)
            #                 )
            #         tag_query = await db.execute(query)
            #         tag_query = tag_query.all()
            #         if not tag_query:
            #             stmt = insert(g_tags).values(
            #                     g_tag_id=uuid.uuid4(),
            #                     name=tag
            #                 )

            #             await db.execute(stmt)
            #             await db.commit()
            # print(result[0][10]) # жанры
            # print(result[0][10])
            # if result[0][10]:
            #     for genre in result[0][10]:
            #         query = (select(
            #                     genres
            #                     ).where(genres.c.name==genre)
            #                 )
            #         genre_query = await db.execute(query)
            #         genre_query = genre_query.all()
            #         if not genre_query:
            #             stmt = insert(genres).values(
            #                     genre_id=uuid.uuid4(),
            #                     name=genre
            #                 )

            #             await db.execute(stmt)
            #             await db.commit()

        # print(result[0][9]) # parent_platform

        # print(result[0][8]) # platform_name
            # if result[0][8]:
            #     for platform in result[0][8]:
            #         for platform_slug in result[0][7]:
            #             query = (select(
            #                         platforms
            #                         ).where(platforms.c.platform_name==platform)
            #                     )
            #             platform_query = await db.execute(query)
            #             platform_query = platform_query.all()
            #             query_slug = (select(
            #                         platforms
            #                         ).where(platforms.c.platform_slug==platform_slug)
            #                     )
            #             platformq_query = await db.execute(query_slug)
            #             platformq_query = platformq_query.all()
            #             if not platform_query:
            #                 if not platformq_query:
            #                     stmt = insert(platforms).values(
            #                             platform_id=uuid.uuid4(),
            #                             platform_name=platform,
            #                             platform_slug=platform_slug
            #                         )

            #                     await db.execute(stmt)
            #                     await db.commit()
            # print(result[0][7]) # platform_slug
            # if result[0][7]:
            #     for platform_slug in result[0][10]:
            #         query = (select(
            #                     platforms
            #                     ).where(platforms.c.platform_slug==platform_slug)
            #                 )
            #         platformq_query = await db.execute(query)
            #         platformq_query = genre_query.all()
            #         if not platformq_query:
            #             stmt = insert(platforms).values(
            #                     platform_id=uuid.uuid4(),
            #                     platform_slug=platform
            #                 )

            #             await db.execute(stmt)
            #             await db.commit()

            offset+=1
            # end_of_base = False
            print(offset)
        else:
            end_of_base = False
