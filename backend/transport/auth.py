from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_async_session
from backend.models.msg import Msg
from backend.authentication.auth import AuthService, get_current_user
from backend.authentication.utils import AuthUtils

from ..models.auth import Token, User, UserCreate

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/sign-up", response_model=Token)
async def sign_up(user_data: UserCreate, service: AuthService = Depends()):
    return await service.registration_user(user_data)


@router.post("/sign-in", response_model=Token)
async def sign_in(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthService = Depends(),
):
    return await service.authenticate_user(form_data.username, form_data.password)


@router.get("/user", response_model=User)
async def get_user(user: User = Depends(get_current_user)):
    return user


@router.post("/recovery-password/{email}", response_model=Msg)
async def recover_password(
    email: str,
    db: AsyncSession = Depends(get_async_session),
    utils: AuthUtils = Depends(),
    service: AuthService = Depends(),
):
    """
    Recovery password
    """
    user = await utils.get_user_by_email(db=db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = await service.create_password_reset_token(email=email)
    print(password_reset_token)
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", response_model=Msg)
async def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: AsyncSession = Depends(get_async_session),
    service: AuthService = Depends(),
    utils: AuthUtils = Depends(),
) -> Any:
    """
    Reset password
    """
    email = await service.verify_password_reset_token(token=token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = await utils.get_user_by_email(db=db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    hashed_password = await service.hash_password(new_password)
    await utils.update_user_password(db=db, password=hashed_password, email=email)
    return {"msg": "Password updated successfully"}


@router.patch('/update-user', response_model=Msg)
async def update_user(user: User = Depends(get_current_user),
                      name: str = Body(...),
                      new_password: str = Body(...),) -> Any:
    print(user)
    print(name)
    print(new_password)
    return{"msg": "Password updated successfully"}
    