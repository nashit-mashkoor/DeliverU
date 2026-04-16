from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ItemCreateRequest(BaseModel):
    """Request model for creating an item"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)


class ItemUpdateRequest(BaseModel):
    """Request model for updating an item"""
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_active: Optional[bool] = None


class ItemResponse(BaseModel):
    """Response model for item information"""
    uuid: str
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime


class ItemListResponse(BaseModel):
    """Response model for paginated item list"""
    items: list[ItemResponse]
    total: int
    limit: int
    offset: int
