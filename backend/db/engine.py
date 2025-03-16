from fastapi import Depends

from db.config import settings

from collections.abc import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from fastapi_users.db import SQLAlchemyUserDatabase

from db.models.user import User

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


def camel_case_to_snake_case(input_str: str) -> str:
    """
    camel_case_to_snake_case("SomeSDK")
    'some_sdk'

    camel_case_to_snake_case("RServoDrive")
    'r_servo_drive'

    camel_case_to_snake_case("SDKDemo")
    'sdk_demo'
    """
    chars = []
    for c_idx, char in enumerate(input_str):
        if c_idx and char.isupper():
            nxt_idx = c_idx + 1
            # idea of the flag is to separate abbreviations
            # as new words, show them in lower case
            flag = nxt_idx >= len(input_str) or input_str[nxt_idx].isupper()
            prev_char = input_str[c_idx - 1]
            if prev_char.isupper() and flag:
                pass
            else:
                chars.append("_")
        chars.append(char.lower())
    return "".join(chars)


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"

    id: Mapped[int] = mapped_column(primary_key=True)


# prod
async def create_db_and_tables():
    async with async_session_maker.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


# test
async def create_test_db_and_tables():
    async with test_async_session_maker.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_test_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session_maker() as session:
        yield session


async def get_test_user_db(session: AsyncSession = Depends(get_test_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
