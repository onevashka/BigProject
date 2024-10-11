from inspect import stack
from typing import Annotated

from alembic.util import status
from fastapi import APIRouter, Depends, HTTPException, status
from .utils import oauth2_scheme, get_current_user,get_current_active_user, \
    authenticate_user, get_password_hash
from .schemas import SUser, SUserInDB, Token, SCreateUserInDB
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from api.config import ACCESS_TOKEN_EXPIRE_MINUTES
from .utils import create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from .models import User


app = APIRouter(tags=['auth'])


@app.get("/user/me")
async def read_items(current_user: Annotated[SUser, Depends(get_current_active_user)]):
    return current_user





@app.post('/token', response_model=None)
async def login_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                             db: AsyncSession = Depends(get_db)) -> Token:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password',
            headers={"WWW-Authenticate": 'Bearer'},

        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.post('/register', response_model=None)
async def register(current_user: SCreateUserInDB, db: AsyncSession = Depends(get_db) ) -> dict:

    hashed_password = get_password_hash(current_user.password)
    new_user = User(
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        hashed_password=hashed_password)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {'message': 'Registration! Ok!'}


@app.get('/readme', response_model=SUser)
async def read_me(current_user: Annotated[SUser, Depends(get_current_active_user)]):
    if not current_user:
        raise HTTPException(status_code=404, detail='User not found')

    return current_user


