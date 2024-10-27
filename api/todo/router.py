from venv import create
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from database.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from .service import ToDO
from api.auth.utils import get_current_active_user
from api.auth.schemas import SUser


app = APIRouter(prefix='/task', tags=['ToDo'])


@app.get('/')
async def get_task(current_user: Annotated[SUser, Depends(get_current_active_user)], db: AsyncSession = Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=404, detail='User not found')
    result = await ToDO.get_task(db=db)
    return result


@app.post('/')
async def create_task(title: str, db: AsyncSession = Depends(get_db)):
    result = await ToDO.create_task(title=title, db=db)
    return result


@app.delete('/{task_id}')
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await ToDO.delete_task(task_id=task_id, db=db)
    return result


@app.patch('/{task_id}')
async def patch_task(title: str, task_id: int, db: AsyncSession = Depends(get_db)):
    result = await ToDO.patch_task(title=title, task_id=task_id, db=db)
    return result

