import datetime
import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from api.authentication.auth import get_current_user
from api.authentication.utils import AuthUtils
from api.database import get_async_session
from api.integrations.get_user_img import get_user_img
from api.models.auth_models import User
from api.services.img_resize import resize_image
from api.services.user_img_upload import save_upload_cover
from api.integrations.users import change_user_data
from api.models.users import UserData
from api.models.msg_models import Msg

router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.post(
    '/change/photo',
    description='Обновление фото профиля, в базу сохраняется 200х200 картинка',
)
async def update_user_photo(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    utils: AuthUtils = Depends(),
    db: AsyncSession = Depends(get_async_session),
):
    if not await utils.is_verified(user):
        raise HTTPException(status_code=400, detail='User not verified')

    file.filename = f'{uuid.uuid4()}.jpg'
    contents = await file.read()  # <-- Important!
    upload_dir = save_upload_cover(
        contents=contents,
        filename=file.filename,
        username=user.username,
    )

    background_tasks.add_task(
        resize_image,
        filename=file.filename,
        path_file=upload_dir,
        db=db,
        id=user.id,
    )
    return {'filename': file.filename}


@router.get(
    '/{id}/get/photo/',
    description='Получение фото профиля пользователя по id',
)
async def get_user_photo_router(
    id: UUID4,
    db: AsyncSession = Depends(get_async_session),
):
    user_img = await get_user_img(db=db, id=id)
    path = user_img[0]
    print(path[0])
    return FileResponse(path[0])


@router.post(
    '/change/about/me/',
    description='Обновление информации из раздела "обо мне", имя, биография, дата рождения',
    response_model=Msg
)
async def update_user_info_router(
    user_data: UserData,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    result = await change_user_data(id=user.id,name=user_data.name, bio=user_data.bio, birthdate=user_data.birthdate, db=db)
    if result:
        return {'msg': 'User data update success'}
    return {'msg': 'Something went wrong'}
