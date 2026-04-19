from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from backend.constants import DATABASE_URL

__all__ = ["AsyncSessionLocal", "async_engine", "get_db"]


async_engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get a request-scoped database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
