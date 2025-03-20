from fastapi import APIRouter
from api.routes.fastapi_users import fastapi_users
from schemas.user import UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])

# /me
# /{id}
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate)
)