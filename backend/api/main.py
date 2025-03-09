from fastapi import APIRouter

from api.routes import detector


api_router = APIRouter()
api_router.include_router(detector.router, tags=["detector"])
