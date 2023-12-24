
from typing import Any
import uuid
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.database import game_table
import datetime as DT
import requests


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
