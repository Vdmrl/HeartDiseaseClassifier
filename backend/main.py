# poetry run uvicorn main:app

import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
# from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from services.classifaer import Classifier

from api.main import api_router

from logger import logger

from services.classifaer import Classifier
from types import SimpleNamespace


app = FastAPI(title="heart disease detector")
app.state = SimpleNamespace()
app.mount("/static", StaticFiles(directory="static"), name="static")


# middleware
origins = [
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:8501",
    "http://frontend:8501",
    "http://backend:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PATCH", "DELETE", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request execution time", extra={
        "process_time": round(process_time, 4)
    })
    response.headers["X-Process-Time"] = str(process_time)
    return response

# cache

@app.on_event("startup")
async def startup():
    logger.info("Starting redis cache...")
    redis = aioredis.from_url("redis://redis:6379", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    logger.info("Redis cache started successfully")

    logger.info("Initializing classifier model...")
    app.state.classifier = Classifier()
    logger.info("Classifier model Initializing successfully")

# routers
app.include_router(api_router)
