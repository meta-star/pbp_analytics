from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import analyze
from app.scheduler import start_scheduler, stop_scheduler
from app.database import engine
from app.models import SQLModel
from app.config import settings
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    start_scheduler()

    # Auto-creation of tables is removed in favor of Alembic migrations.
    # However, for local development convenience or if explicitly requested via env, we might keep it.
    # For this submission, we strictly follow the migration path.
    # async with engine.begin() as conn:
    #      await conn.run_sync(SQLModel.metadata.create_all)

    yield

    # Shutdown
    stop_scheduler()

app = FastAPI(
    title="Phishing Blocker Analytics",
    version="2.0.0",
    description="PBP Analytics with Deep Learning and FastAPI",
    lifespan=lifespan
)

app.include_router(analyze.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
