from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repositories.sqlalchemy_models import ItemModel
from app.core.domain.item import Item
from app.core.ports.item_repository import ItemRepository


class SQLAlchemyItemRepository(ItemRepository):
    """SQLAlchemy implementation of the ItemRepository port."""
    
    def __init__(self, session: AsyncSession):
        """Initialize the repository with a database session.
        
        Args:
            session: SQLAlchemy async session
        """
        self.session = session
    
    async def get(self, id: Any) -> Item | None:
        """Get an item by ID.
        
        Args:
            id: Item ID
            
        Returns:
            Item | None: Item if found, None otherwise
        """
        result = await self.session.execute(
            select(ItemModel).where(ItemModel.id == id)
        )
        db_item = result.scalars().first()
        
        if db_item is None:
            return None
            
        return Item.model_validate(db_item)
    
    async def get_all(self, **kwargs) -> list[Item]:
        """Get all items, with optional filtering.
        
        Args:
            **kwargs: Filter parameters
            
        Returns:
            list[Item]: List of items
        """
        query = select(ItemModel)
        
        # Apply filters if provided
        for key, value in kwargs.items():
            if hasattr(ItemModel, key):
                query = query.where(getattr(ItemModel, key) == value)
                
        result = await self.session.execute(query)
        db_items = result.scalars().all()
        
        return [Item.model_validate(db_item) for db_item in db_items]
    
    async def create(self, entity: Item) -> Item:
        """Create a new item.
        
        Args:
            entity: Item to create
            
        Returns:
            Item: Created item
        """
        db_item = ItemModel(
            name=entity.name,
            description=entity.description,
            price=entity.price,
            is_active=entity.is_active
        )
        
        self.session.add(db_item)
        await self.session.commit()
        await self.session.refresh(db_item)
        
        return Item.model_validate(db_item)
    
    async def update(self, id: Any, entity: Item) -> Item | None:
        """Update an existing item.
        
        Args:
            id: Item ID
            entity: Updated item data
            
        Returns:
            Item | None: Updated item if found, None otherwise
        """
        # Check if item exists
        result = await self.session.execute(
            select(ItemModel).where(ItemModel.id == id)
        )
        db_item = result.scalars().first()
        
        if db_item is None:
            return None
            
        # Update item
        update_data = entity.model_dump(
            exclude={"id", "created_at", "updated_at"}, 
            exclude_none=True
        )
        
        await self.session.execute(
            update(ItemModel)
            .where(ItemModel.id == id)
            .values(**update_data)
        )
        
        await self.session.commit()
        
        # Get updated item
        result = await self.session.execute(
            select(ItemModel).where(ItemModel.id == id)
        )
        updated_db_item = result.scalars().first()
        
        return Item.model_validate(updated_db_item)
    
    async def delete(self, id: Any) -> bool:
        """Delete an item by ID.
        
        Args:
            id: Item ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        result = await self.session.execute(
            delete(ItemModel).where(ItemModel.id == id)
        )
        
        await self.session.commit()
        
        # If no rows were deleted, the item wasn't found
        return result.rowcount > 0
    
    async def find_by_name(self, name: str) -> list[Item]:
        """Find items by name (partial match).
        
        Args:
            name: Item name to search for
            
        Returns:
            list[Item]: List of matching items
        """
        result = await self.session.execute(
            select(ItemModel).where(ItemModel.name.ilike(f"%{name}%"))
        )
        
        db_items = result.scalars().all()
        
        return [Item.model_validate(db_item) for db_item in db_items]
    
    async def find_active_items(self) -> list[Item]:
        """Find all active items.
        
        Returns:
            list[Item]: List of active items
        """
        result = await self.session.execute(
            select(ItemModel).where(ItemModel.is_active is True)
        )
        
        db_items = result.scalars().all()
        
        return [Item.model_validate(db_item) for db_item in db_items] 