from sys import prefix
from typing import Annotated
from .utils import get_user_by_static_auth_token
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials


app = APIRouter(prefix='/auth', tags=['auth'])

security = HTTPBasic()

@app.get('/')
async def basic_auth_credentials(
        username: str = Depends(get_user_by_static_auth_token)
):

    return {"message": f"Hello, {username}! You are authenticated."}
