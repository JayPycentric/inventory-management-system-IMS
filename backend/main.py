from _collections_abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api.routes import api_router
from backend.core.config import settings
from backend.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await init_db()
    yield


app = FastAPI(
    title=settings.APP_TITLE,
    lifespan=lifespan,
)

app.include_router(api_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
