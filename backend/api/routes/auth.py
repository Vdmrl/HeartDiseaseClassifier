from fastapi import APIRouter
from api.routes.fastapi_users import fastapi_users
from api.dependencies.authentication.backend import authentication_backend
from schemas.user import UserRead, UserCreate

router = APIRouter(prefix="/auth", tags=["Auth"])

# /login
# /logout
router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
        requires_verification=False
    ),
)

# /register
router.include_router(
    router=fastapi_users.get_register_router(UserRead, UserCreate),
)

# /request-verify-token
# /verify
router.include_router(
    router=fastapi_users.get_verify_router(UserRead),
)

# /forgot-password
# /reset-password
router.include_router(
    router=fastapi_users.get_reset_password_router()
)