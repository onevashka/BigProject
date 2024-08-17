from sqlalchemy import select
from sqlalchemy.ext.asyncio import  AsyncSession
from database.models import Task



async def get_task_utils(db: AsyncSession):
    query = await db.execute(select(Task))
    tasks = query.scalars().all()
    return tasks


async  def create_task_utils(title: str, db: AsyncSession):
    if title:
        new_task = Task(tittle=title)
        db.add(new_task)
        await  db.commit()
        await  db.refresh(new_task)
        return  {

            'message': 'Task created successfull'

        }
    return {

        'message': 'title is None'

    }

async def delete_task_utils(task_id: int, db: AsyncSession):
    task = await db.get(Task,  task_id)

    if task:
        await db.delete(task)
        await db.commit()
        return {'message': 'Task deleted successfully'}
    return {'message': 'Task not found'}


async def patch_task_utils(title: str ,task_id: int, db: AsyncSession):
    old_task = await db.get(Task, task_id)

    if old_task:
        old_task.tittle = title
        await db.commit()
        await db.refresh(old_task)
        return {'message': 'Task update successfully'}
    return {'message': 'Task not found'}
