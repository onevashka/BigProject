from typing import Annotated
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from .models import AuthToken, User


security = HTTPBasic()


async def get_user_by_static_auth_token(
        auth_token: str = Header(alias='x=auth_token'),
        db: AsyncSession = Depends(get_db)
) -> str:
    result_db = await db.get(AuthToken, auth_token)

    if not result_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid authentication token')

    user = await db.get(User, result_db.user_id)
    return f'Hello, {user.username}'

