from sqlalchemy import func
from sqlmodel import select

from backend.database.models import Item
from backend.database.session import AsyncSessionLocal
from backend.modules.items.item_dto import (
    ItemCreateRequest,
    ItemListResponse,
    ItemResponse,
    ItemUpdateRequest,
)
from backend.utils.exceptions import NotFoundError
from backend.utils.logging import Logging

logging_instance = Logging()
logger = logging_instance.get_logger()


class ItemService:
    """Service for item CRUD operations"""

    async def create_item(self, user_id: int, request: ItemCreateRequest) -> ItemResponse:
        """Create a new item"""
        logger.info("Creating new item", extra={"user_id": user_id, "name": request.name})

        async with AsyncSessionLocal() as session:
            item = Item(name=request.name, description=request.description, user_id=user_id)
            session.add(item)
            await session.commit()
            await session.refresh(item)

            logger.info("Item created successfully", extra={"item_id": item.id})

            return ItemResponse(
                uuid=item.uuid,
                name=item.name,
                description=item.description,
                is_active=item.is_active,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )

    async def get_item(self, user_id: int, item_uuid: str) -> ItemResponse:
        """Get an item by UUID"""
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Item).where(Item.uuid == item_uuid, Item.user_id == user_id))
            item = result.scalar_one_or_none()

            if not item:
                raise NotFoundError("Item", item_uuid)

            return ItemResponse(
                uuid=item.uuid,
                name=item.name,
                description=item.description,
                is_active=item.is_active,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )

    async def list_items(self, user_id: int, limit: int = 100, offset: int = 0) -> ItemListResponse:
        """List all items for a user with pagination"""
        async with AsyncSessionLocal() as session:
            total_result = await session.execute(select(func.count()).select_from(Item).where(Item.user_id == user_id))
            total = int(total_result.scalar_one())
            items_result = await session.execute(
                select(Item)
                .where(Item.user_id == user_id)
                .order_by(Item.created_at.desc(), Item.id.desc())
                .offset(offset)
                .limit(limit)
            )
            items = list(items_result.scalars().all())

            return ItemListResponse(
                items=[
                    ItemResponse(
                        uuid=item.uuid,
                        name=item.name,
                        description=item.description,
                        is_active=item.is_active,
                        created_at=item.created_at,
                        updated_at=item.updated_at,
                    )
                    for item in items
                ],
                total=total,
                limit=limit,
                offset=offset,
            )

    async def update_item(self, user_id: int, item_uuid: str, request: ItemUpdateRequest) -> ItemResponse:
        """Update an item"""
        logger.info("Updating item", extra={"user_id": user_id, "item_uuid": item_uuid})

        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Item).where(Item.uuid == item_uuid, Item.user_id == user_id))
            item = result.scalar_one_or_none()

            if not item:
                raise NotFoundError("Item", item_uuid)

            # Update fields that were provided
            update_data = request.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(item, key, value)

            session.add(item)
            await session.commit()
            await session.refresh(item)

            logger.info("Item updated successfully", extra={"item_id": item.id})

            return ItemResponse(
                uuid=item.uuid,
                name=item.name,
                description=item.description,
                is_active=item.is_active,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )

    async def delete_item(self, user_id: int, item_uuid: str) -> dict:
        """Delete an item"""
        logger.info("Deleting item", extra={"user_id": user_id, "item_uuid": item_uuid})

        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Item).where(Item.uuid == item_uuid, Item.user_id == user_id))
            item = result.scalar_one_or_none()

            if not item:
                raise NotFoundError("Item", item_uuid)

            await session.delete(item)
            await session.commit()

            logger.info("Item deleted successfully", extra={"item_uuid": item_uuid})
            return {"message": "Item deleted successfully"}
