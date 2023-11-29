import os
from random import randint
import shutil
from typing import Annotated, Any
import uuid

from fastapi import APIRouter, BackgroundTasks, Body, Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from dudesplay_api.authentication.auth import AuthService, get_current_user
from dudesplay_api.authentication.utils import AuthUtils
from dudesplay_api.database import get_async_session
from dudesplay_api.integrations.get_user_img import get_user_img
from dudesplay_api.models.auth_models import User
from dudesplay_api.models.msg_models import Msg, VerifyToken
from dudesplay_api.services.user_img_upload import save_upload_cover
from dudesplay_api.services.img_resize import resize_image


router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.patch("/update-user-img", description='Обновление фото профиля, в базу сохраняется 200х200 картинка')
async def update_user_data(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    utils: AuthUtils = Depends(),
    db: AsyncSession = Depends(get_async_session),
):
    if not await utils.is_verified(user):
        raise HTTPException(status_code=400, detail="User not verified")
    
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()  # <-- Important!
    upload_dir = save_upload_cover(contents=contents, filename=file.filename, username=user.username)

    background_tasks.add_task(resize_image, filename=file.filename, path_file=upload_dir, db=db, user_id=user.user_id)
    return {"filename": file.filename}


@router.get("/get-user-img/{user_id}", description='Получение фото профиля пользователя по id')
async def get_user_img_router(user_id: UUID4, db: AsyncSession = Depends(get_async_session)):
    user_img = await get_user_img(db=db, user_id=user_id)
    path = user_img[0]
    print(path[0])
    return FileResponse(path[0])