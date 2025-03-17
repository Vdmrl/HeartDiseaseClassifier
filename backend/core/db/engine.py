from core.config import settings

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.db.models.base import Base

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False,
)

test_async_engine = create_async_engine(
    url=settings.TEST_DATABASE_URL_asyncpg,
    echo=False,
)

async_session_maker = async_sessionmaker(async_engine)
test_async_session_maker = async_sessionmaker(test_async_engine)


# prod
async def create_db_and_tables():
    async with async_session_maker.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


# test
async def create_test_db_and_tables():
    async with test_async_session_maker.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_test_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session_maker() as session:
        yield session
