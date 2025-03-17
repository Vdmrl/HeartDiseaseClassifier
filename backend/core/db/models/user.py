from sqlalchemy.orm import Mapped
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from core.db.engine import Base
from core.db.engine import get_async_session, get_test_async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession



class User(Base, SQLAlchemyBaseUserTable[int]):
    age: Mapped[int]
    pass


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_test_user_db(session: AsyncSession = Depends(get_test_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
