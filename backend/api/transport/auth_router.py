from typing import Annotated, Any

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.authentication.auth import AuthService, get_current_user
from api.authentication.utils import AuthUtils
from api.database import get_async_session
from api.models.msg_models import Msg

from ..models.auth_models import (
    ResetPassword,
    Token,
    User,
    UserCreate,
    UserUpdate,
    VerifyEmail,
    VerifyEmailToken,
)

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/registration', response_model=Token)
async def sign_up(user_data: UserCreate, service: AuthService = Depends()):
    return await service.registration_user(user_data)


@router.post('/login', response_model=Token)
async def sign_in(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthService = Depends(),
):
    return await service.authenticate_user(form_data.username, form_data.password)


@router.get('/user', response_model=User)
async def get_user(user: User = Depends(get_current_user)):
    return user


@router.post('/verify/email/request', response_model=Token)
async def verify_user_email_request(
    email: VerifyEmail, service: AuthService = Depends(),
):
    result = await service.verify_email_request(email=email.email)
    return result


@router.post('/verify/user/email', response_model=Msg)
async def verify_user_email(
    token: VerifyEmailToken,
    service: AuthService = Depends(),
    db: AsyncSession = Depends(get_async_session),
    utils: AuthUtils = Depends(),
):
    user = await service.validate_veify_token(token=token.token)
    if not user:
        raise HTTPException(status_code=400, detail='Invalid token')

    search_user = await utils.get_user_by_email(db=db, email=user.email)
    if not search_user:
        raise HTTPException(status_code=404, detail='User doesnt exist')

    await utils.verify_user_by_email(email=user.email, db=db)
    return {'msg': 'Email verified successfully'}


@router.post('/password/recovery', response_model=Token)
async def recover_password(
    email: VerifyEmail,
    db: AsyncSession = Depends(get_async_session),
    service: AuthService = Depends(),
):
    """
    Recovery password
    """
    result = await service.recover_password(email=email.email)

    return result


@router.post('/password/reset', response_model=Msg)
async def reset_password(
    token: ResetPassword,
    db: AsyncSession = Depends(get_async_session),
    service: AuthService = Depends(),
    utils: AuthUtils = Depends(),
) -> Any:
    """
    Reset password
    """
    user = await service.validate_recover_token(token=token.token)
    if not user:
        raise HTTPException(status_code=400, detail='Invalid token')

    search_user = await utils.get_user_by_email(db=db, email=user.email)

    if not search_user:
        raise HTTPException(status_code=404, detail='User doesnt exist')

    hashed_password = await service.hash_password(token.password)
    await utils.add_new_password(email=user.email, new_password=hashed_password, db=db)
    return {'msg': 'Password updated successfully'}


@router.patch('/update/user', response_model=Msg)
async def update_user_data(
    user_data: UserUpdate = Body(...),
    user: User = Depends(get_current_user),
    utils: AuthUtils = Depends(),
    db: AsyncSession = Depends(get_async_session),
):
    result = await utils.update_user_data(email=user.email, db=db, user=user_data)
    if not result:
        raise HTTPException(status_code=404, detail='Invalid Data')
    return {'msg': 'Data updated successfully'}
