from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app import models  # noqa: F401 - registra os modelos no metadata do SQLAlchemy
from app.routers import auth_router, onboarding_router, block_router, mentor_router, metrics_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Para a PoC, cria as tabelas ausentes ao iniciar. Em produção, prefira migrações Alembic.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    description="API REST do Hub Interativo de Onboarding Técnico RampUp.",
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(onboarding_router.router)
app.include_router(block_router.router)
app.include_router(mentor_router.router)
app.include_router(metrics_router.router)


@app.get("/", tags=["Status"])
def root():
    return {"status": "online", "app": settings.app_name, "docs": "/docs"}


@app.get("/health", tags=["Status"])
def health():
    return {"status": "ok", "service": "RampUp API"}
