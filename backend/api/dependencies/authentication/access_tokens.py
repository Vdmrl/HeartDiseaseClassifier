from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.models import AccessToken
from core.db.engine import get_async_session
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase


async def get_access_token_db(
        session: Annotated[AsyncSession, Depends(get_async_session)],
):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)

