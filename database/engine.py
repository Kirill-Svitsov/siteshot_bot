import os

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from database.models import Base

DATABASE_FILE = os.path.join('data', 'my_base.db')
DATABASE_URL = f'sqlite+aiosqlite:///{DATABASE_FILE}'
# DB_POSTGRES = os.getenv('DB_URL')
DB_POSTGRES = None

if DB_POSTGRES:
    # Если в env указан postgress а формате:
    # postgresql+asyncpg://login:password@localhost:5432/db_name
    engine = create_async_engine(DB_POSTGRES, echo=True)
else:
    # Иначе работает с SQLite
    engine = create_async_engine(
        DATABASE_URL,
        echo=True
    )

session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin as conn:
        await conn.run_sync(Base.metadata.drop_all)
