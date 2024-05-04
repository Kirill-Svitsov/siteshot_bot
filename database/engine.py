import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .models import Base, User, Screenshot, UserLog

DB_LITE = os.getenv('DB_LITE')

if DB_LITE:
    engine = create_async_engine(DB_LITE, echo=True)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin as conn:
        await conn.run_sync(Base.metadata.drop_all)
