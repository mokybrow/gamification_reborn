import uuid

from PIL import Image, ImageOps
from pydantic import UUID4
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.database import profile_pictures, user_table


async def resize_image(filename: str, path_file: str, db: AsyncSession, id: UUID4):
    im = Image.open(path_file + '/' + filename)
    im = ImageOps.exif_transpose(im)
    rgb_im = im.convert('RGB')
    rgb_im.save(path_file + '/' + filename)
    size = (200, 200)
    im = Image.open(path_file + '/' + filename, mode='r')
    ImageOps.fit(im, size).save(path_file + '/' + str(size[0]) + '_' + filename)

    query = select(profile_pictures).where(profile_pictures.c.user_id == id)
    result = await db.execute(query)
    result = result.all()
    if result:
        stmt = (
            update(profile_pictures)
            .values(
                picture_path=path_file + '/' + str(size[0]) + '_' + filename, og_picture_path=path_file + '/' + filename
            )
            .where(profile_pictures.c.user_id == id)
        )
        await db.execute(stmt)
        await db.commit()
        return None
    stmt = insert(profile_pictures).values(
        id=uuid.uuid4(),
        user_id=id,
        picture_path=path_file + '/' + str(size[0]) + '_' + filename,
        og_picture_path=path_file + '/' + filename,
    )
    await db.execute(stmt)
    await db.commit()
