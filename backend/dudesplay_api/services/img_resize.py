from PIL import Image, ImageOps
from pydantic import UUID4
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.database import user_table


async def resize_image(filename: str, path_file: str, db: AsyncSession, user_id: UUID4):
    im = Image.open(path_file + '/' + filename)
    im = ImageOps.exif_transpose(im)
    rgb_im = im.convert('RGB')
    rgb_im.save(path_file + '/' + filename)
    size = (200, 200)
    im = Image.open(path_file + '/' + filename, mode='r')
    ImageOps.fit(im, size).save(path_file + '/' + str(size[0]) + '_' + filename)

    stmt = (
        update(user_table)
        .values(
            profile_picture=path_file + '/' + str(size[0]) + '_' + filename,
        )
        .where(user_table.c.user_id == user_id)
    )
    await db.execute(stmt)
    await db.commit()
