from typing import Annotated

from fastapi import Depends
from fastapi_users.authentication.strategy.db import (
    AccessTokenDatabase, DatabaseStrategy
)

from core.db.models import AccessToken
from api.dependencies.authentication.access_tokens import get_access_token_db

from core.config import settings


def get_database_strategy(
        access_token_db: Annotated[
            AccessTokenDatabase[AccessToken],
            Depends(get_access_token_db)
        ]
) -> DatabaseStrategy:
    return DatabaseStrategy(database=access_token_db, lifetime_seconds=settings.ACCESS_TOKEN_LIFETIME_SECONDS)
