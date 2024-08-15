from sqlalchemy import select
from sqlalchemy.ext.asyncio import  AsyncSession
from api.database.models import Task



async def get_task(db: AsyncSession):
    query = await db.execute(select(Task))
    tasks = query.scalars().all()
    return tasks


async  def create_task(title: str, db: AsyncSession) -> dict:
    if title:
        new_task = Task(title=title)
        db.add(new_task)
        await  db.commit()
        await  db.refresh(new_task)
        return  {

            'message': 'Task created successfull'

        }
    return {

        'message': 'title is None'

    }

async def delete_task(task_id: str, db: AsyncSession) -> dict:
    task = await db.get(Task,  task_id)

    if task:
        await db.delete(task)
        await db.commit()
        return {'message': 'Task deleted successfully'}
    return {'message': 'Task not found'}


async def patch_task(title: str ,task_id: int, db: AsyncSession) -> dict:
    old_task = await db.get(Task, task_id)

    if old_task:
        old_task.title = title
        await db.commit()
        await db.refresh(old_task)
        return {'message': 'Task update successfully'}
    return {'message': 'Task not found'}
