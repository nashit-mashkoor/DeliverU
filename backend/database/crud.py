import contextlib
from typing import Any, AsyncGenerator, Dict, List, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from backend.constants import DATABASE_URL

# Create async engine
async_engine = create_async_engine(DATABASE_URL, echo=False)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

T = TypeVar("T", bound="EasyModel")


class EasyModel(SQLModel):
    """Base model with common CRUD operations"""

    @classmethod
    @contextlib.asynccontextmanager
    async def get_session(cls) -> AsyncGenerator[AsyncSession, None]:
        """Provide a transactional scope around a series of operations."""
        async with AsyncSessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    @classmethod
    async def create(cls: Type[T], session: AsyncSession, **kwargs: Any) -> T:
        """Create a new instance of the model"""
        instance = cls(**kwargs)
        session.add(instance)
        return instance

    @classmethod
    async def get_by_id(cls: Type[T], session: AsyncSession, id: int) -> Optional[T]:
        """Get an instance by ID"""
        statement = select(cls).where(cls.id == id)
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    @classmethod
    async def get_by_uuid(cls: Type[T], session: AsyncSession, uuid_value: str) -> Optional[T]:
        """Get an instance by UUID"""
        statement = select(cls).where(cls.uuid == uuid_value)
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls: Type[T], session: AsyncSession, limit: int = 100, offset: int = 0) -> List[T]:
        """Get all instances with pagination"""
        statement = select(cls).limit(limit).offset(offset)
        result = await session.execute(statement)
        return list(result.scalars().all())

    @classmethod
    async def filter(cls: Type[T], session: AsyncSession, **kwargs: Any) -> List[T]:
        """Filter instances by given criteria"""
        statement = select(cls)
        for key, value in kwargs.items():
            statement = statement.where(getattr(cls, key) == value)
        result = await session.execute(statement)
        return list(result.scalars().all())

    @classmethod
    async def update_by_id(cls: Type[T], session: AsyncSession, id: int, **kwargs: Any) -> Optional[T]:
        """Update an instance by ID"""
        statement = select(cls).where(cls.id == id)
        result = await session.execute(statement)
        instance = result.scalar_one_or_none()

        if not instance:
            return None

        for key, value in kwargs.items():
            setattr(instance, key, value)

        session.add(instance)
        return instance

    @classmethod
    async def delete_by_id(cls: Type[T], session: AsyncSession, id: int) -> bool:
        """Delete an instance by ID"""
        statement = select(cls).where(cls.id == id)
        result = await session.execute(statement)
        instance = result.scalar_one_or_none()

        if not instance:
            return False

        await session.delete(instance)
        return True

    @classmethod
    async def get_or_create(
        cls: Type[T], session: AsyncSession, defaults: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> tuple[T, bool]:
        """Get an existing instance or create a new one"""
        statement = select(cls)
        for key, value in kwargs.items():
            statement = statement.where(getattr(cls, key) == value)

        result = await session.execute(statement)
        instance = result.scalar_one_or_none()

        if instance:
            return instance, False

        create_data = {**kwargs}
        if defaults:
            create_data.update(defaults)

        instance = cls(**create_data)
        session.add(instance)
        return instance, True


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_models() -> None:
    """Deprecated bootstrap helper; use Alembic migrations instead."""
    raise RuntimeError("Database initialization must run through Alembic migrations (make migrate)")
