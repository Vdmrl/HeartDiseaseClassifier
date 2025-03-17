from core.auth.user_manager import UserManager
from .users import get_user_db
from typing import Annotated
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase


async def get_user_manager(user_db: Annotated[SQLAlchemyUserDatabase, Depends(get_user_db)]):
    yield UserManager(user_db)
