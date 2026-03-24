from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.api.report import router as report_router
from app.core.config import settings
from app.core.logging_config import setup_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    settings.setup_dirs()
    logger.info("app started")
    yield
    logger.info("app shutdown")

app = FastAPI(lifespan=lifespan)

app.include_router(report_router)


@app.get("/ping")
async def ping():
    return {"status": "ok"}