from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from api.config import *


URL = f'postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

Base = declarative_base()

engine = create_async_engine(URL, echo=True)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession)

async def get_db():
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        raise e
    finally:
        await session.close()

        

