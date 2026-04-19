from typing import Dict

from fastapi import APIRouter, Depends, Query, status

from backend.modules.items.item_dto import (
    ItemCreateRequest,
    ItemListResponse,
    ItemResponse,
    ItemUpdateRequest,
)
from backend.modules.items.item_service import ItemService
from backend.services.security import JWTBearer

item_router = APIRouter(prefix="/api/v1/items", tags=["Items"])
item_service = ItemService()
security = JWTBearer()


@item_router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(request: ItemCreateRequest, current_user: dict = Depends(security)) -> ItemResponse:
    """Create a new item."""
    return await item_service.create_item(user_id=current_user["user_id"], request=request)


@item_router.get("", response_model=ItemListResponse)
async def list_items(
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    current_user: dict = Depends(security),
) -> ItemListResponse:
    """List all items for the current user with pagination."""
    return await item_service.list_items(user_id=current_user["user_id"], limit=limit, offset=offset)


@item_router.get("/{item_uuid}", response_model=ItemResponse)
async def get_item(item_uuid: str, current_user: dict = Depends(security)) -> ItemResponse:
    """Get a specific item by UUID."""
    return await item_service.get_item(user_id=current_user["user_id"], item_uuid=item_uuid)


@item_router.patch("/{item_uuid}", response_model=ItemResponse)
async def update_item(
    item_uuid: str, request: ItemUpdateRequest, current_user: dict = Depends(security)
) -> ItemResponse:
    """Update an item."""
    return await item_service.update_item(user_id=current_user["user_id"], item_uuid=item_uuid, request=request)


@item_router.delete("/{item_uuid}", response_model=Dict[str, str])
async def delete_item(item_uuid: str, current_user: dict = Depends(security)) -> Dict[str, str]:
    """Delete an item."""
    return await item_service.delete_item(user_id=current_user["user_id"], item_uuid=item_uuid)
