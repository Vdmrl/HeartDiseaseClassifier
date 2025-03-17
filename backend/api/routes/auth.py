from fastapi import APIRouter, File, UploadFile, status, HTTPException
from api.dependencies.authentication.fastapi_users import fastapi_users
from api.dependencies.authentication.backend import authentication_backend
from schemas.user import UserRead, UserCreate

router = APIRouter(prefix="/auth", tags=["Auth"])

# /login
# /logout
router.include_router(
    router=fastapi_users.get_auth_router(authentication_backend),
)

# /register
router.include_router(
    router=fastapi_users.get_register_router(UserRead, UserCreate)
)
