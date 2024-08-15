from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from api.config import *


URL = f'postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

Base = declarative_base()

engine = create_async_engine(URL)

SessionLocal = sessionmaker(bind=engine, _class = AsyncSession)

async def get_db():
    try:
        session = SessionLocal()
        yield session
    except Exception as e:
        print(e)
    finally:
        await session.close()

        

