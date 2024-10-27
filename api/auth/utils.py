import jwt
from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import Depends, FastAPI, status, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBasic
from database.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .schemas import SUser, SUserInDB, Token, TokenData
from passlib.context import CryptContext
from .models import User
from jwt.exceptions import InvalidTokenError
from api.config import SECRET_KEY, ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')



async def get_user(db: AsyncSession, username: str):
    query = select(User).filter(User.username == username)
    result = await db.execute(query)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return SUserInDB(username=user.username, email=user.email, full_name=user.full_name,
                     hashed_password=user.hashed_password, disabled=user.disabled)


#--------------- Hashed password functions

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user

#----------------------------------------------------------------

#----------------- JWT Authentication

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp' : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db)):
    print('ghfghfhfghgfhfghfhgfhfghfghfghfghfg')
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    print(user)
    print('sdfsdfsdfsdfsdfdsfsdfdfsfsdfdsfdsfsdfdsfsdfsdfsfdsfsdfdsfdsffsdfs')
    return user


async def get_current_active_user(current_user: Annotated[SUser, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user
