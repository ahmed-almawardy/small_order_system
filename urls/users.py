from typing import Annotated

from fastapi import APIRouter, Depends, Query, Security
from fastapi.responses import JSONResponse
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from db.repo import create_user, get_users
from forms import UserLoginForm
from schemas import (
    PaginatedResponseSchema,
    TokenPayload,
    TokensResponse,
    UserCreateSchema,
    UserSchema,
)
from services.auth import authenticate_user, get_current_user
from services.common import add_user_blacklist
from services.deps import allow_active_user, allow_anon_user, get_redis

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/", response_model=UserSchema, response_class=JSONResponse)
async def post_user(
    request: UserCreateSchema,
    session: AsyncSession = Depends(get_session),
):
    return await create_user(session, request.model_dump())


@user_router.get(
    "/",
    response_class=JSONResponse,
    response_model=PaginatedResponseSchema[UserSchema],
)
async def list_users(
    session: Annotated[AsyncSession, Depends(get_session)],
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    user=Depends(get_current_user),
):
    users = await get_users(session, limit, offset)
    return {
        "items": users,
        "offset": offset,
        "limit": limit,
        "total": len(users),
    }


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
    "/token",
    response_class=JSONResponse,
    response_model=TokensResponse,
    dependencies=[Depends(allow_anon_user)],
)
async def post_login(
    session: Annotated[AsyncSession, Depends(get_session)],
    auth_form: Annotated[UserLoginForm, Depends()],
):
    """
    Generate JWT Pair of tokens (access, Refresh) per valid request,
    I am not invalidating old tokens, to maintain user access from other devices,
    and they will be expired at a specific time.
    :param session: AsyncSession
    :param auth_form: Form() for authentication
    :return: JSONResponse
    """
    return await authenticate_user(session, auth_form)


@auth_router.get(
    "/me",
    response_class=JSONResponse,
    response_model=TokenPayload,
)
async def get_me(current_user:Annotated[dict, Depends(allow_active_user)]):
    return current_user


@auth_router.get("/logout", status_code=200, response_class=JSONResponse)
async def auth_logout(
    user: Annotated[dict, Security(get_current_user)],
    cache:Annotated[Redis, Depends(get_redis)]
):
    is_active = await add_user_blacklist(user["jti"], cache)
    user.update(is_active=is_active)
    return user
