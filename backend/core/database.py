from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.core.config import Settings, settings


def build_async_engine(app_settings: Settings = settings) -> AsyncEngine:
    return create_async_engine(
        str(app_settings.database_url),
        echo=app_settings.debug,
        pool_pre_ping=True,
        pool_recycle=1800,
    )


engine = build_async_engine()

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)


@asynccontextmanager
async def session_scope() -> AsyncIterator[AsyncSession]:
    """Provide a session and roll back automatically when an operation fails."""
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


async def dispose_engine() -> None:
    """Release all pooled database connections during application shutdown."""
    await engine.dispose()
