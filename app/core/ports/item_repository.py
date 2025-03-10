from typing import List, Optional
from app.core.ports.repositories import Repository
from app.core.domain.item import Item


class ItemRepository(Repository[Item]):
    """Item repository interface.
    
    This is a specific port for the Item entity in the hexagonal architecture.
    """
    
    async def find_by_name(self, name: str) -> List[Item]:
        """Find items by name (partial match).
        
        Args:
            name: Item name to search for
            
        Returns:
            List[Item]: List of matching items
        """
        pass
    
    async def find_active_items(self) -> List[Item]:
        """Find all active items.
        
        Returns:
            List[Item]: List of active items
        """
        pass 