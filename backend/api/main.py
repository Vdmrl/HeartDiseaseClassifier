from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from api.routes import detector
from api.routes import auth
from api.routes import users

http_bearer = HTTPBearer(auto_error=False)

api_router = APIRouter(
    dependencies=[Depends(http_bearer)]
)
api_router.include_router(detector.router)
api_router.include_router(auth.router)
api_router.include_router(users.router)
