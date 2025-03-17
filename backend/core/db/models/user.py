from collections.abc import AsyncGenerator

from sqlalchemy.orm import Mapped
from fastapi_users.db import SQLAlchemyBaseUserTable
from core.engine import Base
from core.engine import AsyncSession, get_async_session, SQLAlchemyUserDatabase, get_test_async_session
from fastapi import Depends


class User(Base, SQLAlchemyBaseUserTable[int]):
    age: Mapped[int]
    pass


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_test_user_db(session: AsyncSession = Depends(get_test_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
