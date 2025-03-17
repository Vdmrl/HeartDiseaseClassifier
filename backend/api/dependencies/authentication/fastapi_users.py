from .user_managers import get_user_manager
from fastapi_users import FastAPIUsers
from core.db.models import User
from .backend import authentication_backend

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [authentication_backend],
)
