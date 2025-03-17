import uuid
from typing import Optional

from fastapi import Request
from fastapi_users import BaseUserManager, IntegerIDMixin

from core.config import settings
from core.db.models import User
from logger import logger

SECRET = "SECRET"


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = settings.VERIFICATION_TOKEN_SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger.warning("User has registered.", extra={"user_id": user.id})

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.warning("User has forgot their password. Reset token.", extra={"user_id": user.id, "token": token})

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.warning("Verification requested for user. Verification token.", extra={"user_id": user.id, "token": token})
