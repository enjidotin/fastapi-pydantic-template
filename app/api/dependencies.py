from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repositories.database import get_session
from app.adapters.repositories.sqlalchemy_item_repository import (
    SQLAlchemyItemRepository,
)
from app.core.ports.item_repository import ItemRepository
from app.core.services.item_service import ItemService


async def get_item_repository(
    session: AsyncSession = Depends(get_session),
) -> ItemRepository:
    """Get an item repository instance.
    
    Args:
        session: Database session
        
    Returns:
        ItemRepository: Repository instance
    """
    return SQLAlchemyItemRepository(session)


async def get_item_service(
    repository: ItemRepository = Depends(get_item_repository),
) -> ItemService:
    """Get an item service instance.
    
    Args:
        repository: Item repository
        
    Returns:
        ItemService: Service instance
    """
    return ItemService(repository) 