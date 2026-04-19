from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models import User, UserRole


class AuthRepository:
    """Database access for the auth module."""

    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[User]:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(
        session: AsyncSession,
        *,
        email: str,
        hashed_password: str,
        role: UserRole,
    ) -> User:
        user = User(email=email, hashed_password=hashed_password, role=role)
        session.add(user)
        await session.flush()
        return user

    @staticmethod
    async def update_password(session: AsyncSession, user: User, hashed_password: str) -> User:
        user.hashed_password = hashed_password
        session.add(user)
        await session.flush()
        return user

    @staticmethod
    async def deactivate_user(session: AsyncSession, user: User) -> User:
        user.is_active = False
        session.add(user)
        await session.flush()
        return user

    @staticmethod
    async def touch_user_updated_at(session: AsyncSession, user: User, updated_at: datetime) -> User:
        user.updated_at = updated_at
        session.add(user)
        await session.flush()
        return user
