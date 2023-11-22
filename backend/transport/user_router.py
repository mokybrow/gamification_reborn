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

from backend.authentication.auth import AuthService, get_current_user
from backend.authentication.utils import AuthUtils
from backend.database import get_async_session
from backend.integrations.get_user_img import get_user_img
from backend.models.msg_models import Msg, VerifyToken
from backend.services.user_img_upload import save_upload_cover
from backend.services.img_resize import resize_image


router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.get("/get-user-img/{user_id}", description='Получение фото профиля пользователя по id')
async def get_user_img_router(user_id: UUID4, db: AsyncSession = Depends(get_async_session)):
    user_img = await get_user_img(db=db, user_id=user_id)
    path = user_img[0]
    print(path[0])
    return FileResponse(path[0])