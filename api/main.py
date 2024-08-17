from fastapi import FastAPI
from todo.router import app as todo_router
from auth.router import app as auth_router


app = FastAPI()
app.include_router(todo_router)
app.include_router(auth_router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)