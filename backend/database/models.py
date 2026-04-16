from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import Column, String
from sqlmodel import Field, Relationship

from backend.database.crud import EasyModel


class User(EasyModel, table=True):
    """User table for authentication"""

    __tablename__ = "user"

    id: int = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid4()), sa_column=Column(String, unique=True))
    email: str = Field(unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    # Relationships
    items: List["Item"] = Relationship(back_populates="user")


class Item(EasyModel, table=True):
    """Example item table - demonstrates CRUD pattern"""

    __tablename__ = "item"

    id: int = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid4()), sa_column=Column(String, unique=True))
    name: str = Field(nullable=False, index=True)
    description: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
    user_id: int = Field(foreign_key="user.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    # Relationships
    user: Optional["User"] = Relationship(back_populates="items")

