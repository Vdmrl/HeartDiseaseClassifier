from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.models import User
from core.db.engine import get_async_session, get_test_async_session
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase


async def get_user_db(
        session: Annotated[AsyncSession, Depends(get_async_session)]
):
    yield SQLAlchemyUserDatabase(session, User)

# async def get_test_user_db(session: Annotated[AsyncSession, Depends(get_async_session)]):
#     yield SQLAlchemyUserDatabase(session, User)
