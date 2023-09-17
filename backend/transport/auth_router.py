from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.authentication.auth import AuthService, get_current_user
from backend.database import get_async_session
from backend.models.msg import Msg

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
    service: AuthService = Depends(),
):
    """
    Recovery password
    """
    abc = await service.recover_password(email=email)

    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", response_model=Msg)
async def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: AsyncSession = Depends(get_async_session),
    service: AuthService = Depends(),
) -> Any:
    """
    Reset password
    """
    abc = await service.validate_recover_token(token=token)
    return {"msg": "Password updated successfully"}
