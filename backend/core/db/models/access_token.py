from fastapi import Depends
from fastapi_users_db_sqlalchemy import Integer
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTable,
)
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped, mapped_column

from core.db.models.base import Base
from core.db.engine import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession

class AccessToken(Base, SQLAlchemyBaseAccessTokenTable[int]):
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="cascade"),
        nullable=False
    )
