from typing import List, Optional
from app.core.domain.item import Item
from app.core.ports.item_repository import ItemRepository


class ItemService:
    """Item service for business logic related to items.
    
    This service is part of the application core and uses the repository
    port to interact with the data layer.
    """
    
    def __init__(self, item_repository: ItemRepository):
        """Initialize the service with a repository.
        
        Args:
            item_repository: Repository implementation for items
        """
        self.repository = item_repository
    
    async def get_item(self, item_id: int) -> Optional[Item]:
        """Get an item by ID.
        
        Args:
            item_id: Item ID
            
        Returns:
            Optional[Item]: Item if found, None otherwise
        """
        return await self.repository.get(item_id)
    
    async def get_all_items(self) -> List[Item]:
        """Get all items.
        
        Returns:
            List[Item]: List of all items
        """
        return await self.repository.get_all()
    
    async def create_item(self, item: Item) -> Item:
        """Create a new item.
        
        Args:
            item: Item to create
            
        Returns:
            Item: Created item
        """
        return await self.repository.create(item)
    
    async def update_item(self, item_id: int, item: Item) -> Optional[Item]:
        """Update an existing item.
        
        Args:
            item_id: Item ID
            item: Updated item data
            
        Returns:
            Optional[Item]: Updated item if found, None otherwise
        """
        return await self.repository.update(item_id, item)
    
    async def delete_item(self, item_id: int) -> bool:
        """Delete an item by ID.
        
        Args:
            item_id: Item ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        return await self.repository.delete(item_id)
    
    async def search_items_by_name(self, name: str) -> List[Item]:
        """Search items by name.
        
        Args:
            name: Item name to search for
            
        Returns:
            List[Item]: List of matching items
        """
        return await self.repository.find_by_name(name)
    
    async def get_active_items(self) -> List[Item]:
        """Get all active items.
        
        Returns:
            List[Item]: List of active items
        """
        return await self.repository.find_active_items()
    
    async def apply_discount_to_item(self, item_id: int, discount_percent: float) -> Optional[Item]:
        """Apply a discount to an item.
        
        Args:
            item_id: Item ID
            discount_percent: Discount percentage (0-100)
            
        Returns:
            Optional[Item]: Updated item if found, None otherwise
        """
        item = await self.repository.get(item_id)
        if not item:
            return None
            
        discounted_price = item.apply_discount(discount_percent)
        item.price = discounted_price
        return await self.repository.update(item_id, item) 