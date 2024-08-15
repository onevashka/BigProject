from venv import create

from fastapi import APIRouter, Depends
from httpx import delete
from pyexpat.errors import messages

from api.database.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from .utils import get_task, patch_task, create_task, delete_task

app = APIRouter(prefix='/task', tags=['ToDo'])


@app.get('/')
async def get_task(db: AsyncSession = Depends(get_db)) -> dict:
    result = await get_task(db=db)
    return result


@app.post('/')
async def create_task(title: str, db: AsyncSession = Depends(get_db)) -> dict:
    result = await create_task(title=title, db=db)
    return result


@app.delete('/{task_id}')
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    result = await delete_task(task_id=task_id, db=db)
    return result


@app.patch('/{task_id}')
async def patch_task(title: str, task_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    result = await patch_task(title=title, task_id=task_id, db=db)
    return result