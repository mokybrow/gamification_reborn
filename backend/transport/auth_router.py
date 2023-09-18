from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.authentication.auth import AuthService, get_current_user
from backend.authentication.utils import AuthUtils
from backend.database import get_async_session
from backend.models.msg import Msg

from ..models.auth import Token, User, UserCreate, UserUpdate, UserUpdateImg

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


@router.post("/verify-email-request/{email}", response_model=Msg)
async def verify_user_email_request(email: str, service: AuthService = Depends()):
    await service.verify_email_request(email=email)
    return {"msg": "Email verification mail sent"}


@router.post("/verify-user-email", response_model=Msg)
async def verify_user_email(
    token: str = Body(...),
    service: AuthService = Depends(),
    db: AsyncSession = Depends(get_async_session),
    utils: AuthUtils = Depends(),
):
    user = await service.validate_veify_token(token=token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    search_user = await utils.get_user_by_email(db=db, email=user.email)
    if not search_user:
        raise HTTPException(status_code=404, detail="User doesnt exist")
    
    await utils.verify_user_by_email(email=user.email, db=db)
    return {"msg": "Password updated successfully"}


@router.post("/recovery-password/{email}", response_model=Msg)
async def recover_password(
    email: str,
    db: AsyncSession = Depends(get_async_session),
    service: AuthService = Depends(),
):
    """
    Recovery password
    """
    await service.recover_password(email=email)

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
    user = await service.validate_recover_token(token=token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    search_user = await utils.get_user_by_email(db=db, email=user.email)
    print(search_user)

    if not search_user:
        raise HTTPException(status_code=404, detail="User doesnt exist")

    hashed_password = await service.hash_password(new_password)
    await utils.add_new_password(email=user.email, new_password=hashed_password, db=db)
    return {"msg": "Password updated successfully"}


@router.patch("/update-user", response_model=Msg)
async def update_user_data(
    user_data: UserUpdate = Body(...),
    user: User = Depends(get_current_user),
    utils: AuthUtils = Depends(),
    db: AsyncSession = Depends(get_async_session),
):
    result = await utils.update_user_data(email=user.email, db=db, user=user_data)
    if not result:
        raise HTTPException(status_code=404, detail="Invalid Data")
    return {"msg": "Data updated successfully"}


@router.patch("/update-user-img", response_model=Msg)
async def update_user_data(
    user_data: UserUpdateImg = Body(...),
    user: User = Depends(get_current_user),
    utils: AuthUtils = Depends(),
    db: AsyncSession = Depends(get_async_session),
):
    print(user)
    if not await utils.is_verified(user):
        raise HTTPException(status_code=400, detail="User not verified")

    result = await utils.update_user_image(email=user.email, db=db, user=user_data)

    if not result:
        raise HTTPException(status_code=404, detail="Invalid Data")
    return {"msg": "Data updated successfully"}
