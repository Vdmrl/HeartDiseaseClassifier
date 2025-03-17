from fastapi import APIRouter

from api.routes import detector
from api.routes import auth


api_router = APIRouter()
api_router.include_router(detector.router)
api_router.include_router(auth.router)
