from venv import create

from fastapi import APIRouter, Depends
from httpx import delete
from pyexpat.errors import messages

from database.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from .utils import get_task_utils, patch_task_utils, create_task_utils, delete_task_utils

app = APIRouter(prefix='/task', tags=['ToDo'])


@app.get('/')
async def get_task(db: AsyncSession = Depends(get_db)):
    result = await get_task_utils(db=db)
    return result


@app.post('/')
async def create_task(title: str, db: AsyncSession = Depends(get_db)):
    result = await create_task_utils(title=title, db=db)
    return result


@app.delete('/{task_id}')
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await delete_task_utils(task_id=task_id, db=db)
    return result


@app.patch('/{task_id}')
async def patch_task(title: str, task_id: int, db: AsyncSession = Depends(get_db)):
    result = await patch_task_utils(title=title, task_id=task_id, db=db)
    return result

