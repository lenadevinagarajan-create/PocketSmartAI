from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.db.database import init_db
from app.routes.auth import router as auth_router
from app.routes.pages import router as pages_router
from app.routes.planners import router as planner_router
from app.routes.session import router as session_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="PocketSmart AI",
    description="Budget-aware AI recommendation assistant for home, party and jewelry planning.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(pages_router)
app.include_router(auth_router, prefix="/api")
app.include_router(session_router, prefix="/api")
app.include_router(planner_router, prefix="/api")

@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "service": "PocketSmart AI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=settings.debug)
