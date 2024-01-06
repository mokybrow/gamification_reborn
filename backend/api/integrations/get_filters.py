import datetime as DT
import uuid

from typing import Any

import requests

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.database import age_rating_games, age_ratings, game_genres, game_platforms, game_table, genres, platforms


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


async def game_parser(db: AsyncSession) -> Any:
    count = 14890
    while count < 50000:
        r = requests.get(
            f'https://api.rawg.io/api/games?key=1ae731eafea74e33907d89607c9483cb&page={count}&page_size=50'
        )
        print(count)
        platform = []
        parent_platforms = []
        platform_name = []
        genres = []
        for i in r.json()['results']:
            for k in i['genres']:
                genres.append(k['name'])

            for q in i['parent_platforms']:
                parent_platforms.append(q['platform']['name'])

            for j in i['platforms']:
                platform.append(j['platform']['slug'])
                platform_name.append(j['platform']['name'])

            query = select(game_table.c.slug).where(game_table.c.slug == i['slug'])
            result = await db.execute(query)
            if result.all():
                pass
            query = select(game_table.c.slug).where(game_table.c.slug == i['slug'])
            result = await db.execute(query)
            if not result.all():
                # print(i['name'], i['background_image'],i['slug'], i['released'], i['parent_platforms'], i['genres'])
                if i['released'] != None:
                    date = DT.datetime.strptime(i['released'], '%Y-%m-%d').date()
                if i['released'] == None:
                    date = None
                if i['esrb_rating'] == None:
                    esrb_rating = None
                if i['esrb_rating'] != None:
                    esrb_rating = i['esrb_rating']['name']
                stmt = insert(game_table).values(
                    id=uuid.uuid4(),
                    title=i['name'],
                    cover=i['background_image'],
                    description=None,
                    slug=i['slug'],
                    release=date,
                    playtime=i['playtime'],
                    platform=platform,
                    platform_name=platform_name,
                    parent_platform=parent_platforms,
                    genre=genres,
                    esrb_rating=esrb_rating,
                )

                await db.execute(stmt)
                await db.commit()
                platform = []
                parent_platforms = []
                platform_name = []
                genres = []
                tags = []

        count += 1


async def norm_data(db: AsyncSession):
    offset = 0
    end_of_base = True
    # while end_of_base:
    #     query = (select(game_table)
    #                     .offset(offset)
    #                     .limit(1))
    #     result = await db.execute(query)
    #     result = result.all()
    #     if result:
    #         print(result[0][0])

    #         # print(result[0][7]) #слаг
    #         # print(result[0][8]) #имя
    #         if result[0][7]:
    #             for name, slug in zip(result[0][8], result[0][7]):
    #                 query_slug = select(platforms.c.platform_slug).where(platforms.c.platform_slug==slug)
    #                 query_slug = await db.execute(query_slug)
    #                 query_slug = query_slug.all()
    #                 if not query_slug:
    #                     stmt = insert(platforms).values(
    #                                     id = uuid.uuid4(),
    #                                     platform_name=name,
    #                                     platform_slug=slug
    #                                 )
    #                     await db.execute(stmt)
    #                     await db.commit()

    #         # print(result[0][10]) #жанр
    #         if result[0][10]:
    #             for genre_name in result[0][10]:
    #                 query_genre = select(genres.c.name).where(genres.c.name==genre_name)
    #                 query_genre = await db.execute(query_genre)
    #                 query_genre = query_genre.all()
    #                 if not query_genre:
    #                     stmt = insert(genres).values(
    #                                     id = uuid.uuid4(),
    #                                     name=genre_name,

    #                                 )
    #                     await db.execute(stmt)
    #                     await db.commit()
    #         # print(result[0][11]) #возрастной рейтинг
    #         if result[0][11]:
    #             query_age = select(age_ratings.c.name).where(age_ratings.c.name==result[0][11])
    #             query_age = await db.execute(query_age)
    #             query_age = query_age.all()
    #             if not query_age:
    #                 stmt = insert(age_ratings).values(
    #                                     id = uuid.uuid4(),
    #                                     name=result[0][11],
    #                                 )
    #                 await db.execute(stmt)
    #                 await db.commit()

    #         offset+=1

    #     else:
    #         end_of_base = False

    while end_of_base:
        ##Добавление возрастных рейтнгов
        query = select(game_table).where(game_table.c.platform != None)
        result = await db.execute(query)
        result = result.all()

        # print(check_pair)
        if result:
            for j in result:
                # if j[11]:
                #     age_rate_id = (select(age_ratings).where(age_ratings.c.name==j[11]))
                #     age_rate_id = await db.execute(age_rate_id)
                #     age_rate_id = age_rate_id.all()
                #     check_pair = (select(age_rating_games).where(age_rating_games.c.game_id==j[0], age_rating_games.c.age_rating_id==age_rate_id[0][0]))
                #     check_pair = await db.execute(check_pair)
                #     check_pair = check_pair.all()
                #     if not check_pair:
                #         # print(result[0][11])
                #         # print(result[0][0])
                #         # print(age_rate_id[0][0])
                #         stmt = insert(age_rating_games).values(
                #                                     id = uuid.uuid4(),
                #                                     game_id=j[0],
                #                                     age_rating_id=age_rate_id[0][0]
                #                                 )
                #         await db.execute(stmt)
                #         await db.commit()
                # # ##Добавление жанров

                # if j[10]:
                #     end_of_base = False
                #     for genre in j[10]:
                #         genre_id = (select(genres).where(genres.c.name==genre))
                #         genre_id = await db.execute(genre_id)
                #         genre_id = genre_id.all()
                #         check_pair = (select(game_genres).where(game_genres.c.game_id==j[0], game_genres.c.genre_id==genre_id[0][0]))
                #         check_pair = await db.execute(check_pair)
                #         check_pair = check_pair.all()
                #         if not check_pair:
                #                 # print(result[0][11])
                #                 # print(result[0][0])
                #                 # print(age_rate_id[0][0])
                #                 stmt = insert(game_genres).values(
                #                                             id = uuid.uuid4(),
                #                                             game_id=j[0],
                #                                             genre_id=genre_id[0][0]
                #                                         )
                #                 await db.execute(stmt)
                #                 await db.commit()
                # # ##Добавление платформ
                if j[7]:
                    end_of_base = False
                    for platform in j[7]:
                        platform_id = select(platforms).where(platforms.c.platform_slug == platform)
                        platform_id = await db.execute(platform_id)
                        platform_id = platform_id.all()
                        check_pair = select(game_platforms).where(
                            game_platforms.c.game_id == j[0], game_platforms.c.platform_id == platform_id[0][0]
                        )
                        check_pair = await db.execute(check_pair)
                        check_pair = check_pair.all()
                        if not check_pair:
                            # print(result[0][11])
                            # print(result[0][0])
                            # print(age_rate_id[0][0])
                            stmt = insert(game_platforms).values(
                                id=uuid.uuid4(), game_id=j[0], platform_id=platform_id[0][0]
                            )
                            await db.execute(stmt)
                            await db.commit()
                # if result:
                #     print(result[0][7])
            print(offset)
            offset += 1
        else:
            end_of_base = False
