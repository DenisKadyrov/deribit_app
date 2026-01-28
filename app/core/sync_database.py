from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


def _make_sync_url(async_url: str) -> str:
    # e.g. postgresql+asyncpg:// -> postgresql://
    if "+asyncpg" in async_url:
        return async_url.replace("+asyncpg", "")
    return async_url


SYNC_DATABASE_URL = _make_sync_url(settings.DATABASE_URL)

engine = create_engine(SYNC_DATABASE_URL, future=True)

SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, class_=Session
)
