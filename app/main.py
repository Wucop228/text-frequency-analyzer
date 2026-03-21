from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.report import router as report_router
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings.setup_dirs()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(report_router)


@app.get("/ping")
async def ping():
    return {"status": "ok"}