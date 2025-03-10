from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar('T')


class Repository(Generic[T], ABC):
    """Abstract base repository interface.
    
    This is a port in the hexagonal architecture that defines
    how the application core interacts with external data sources.
    """
    
    @abstractmethod
    async def get(self, id: Any) -> T | None:
        """Get an entity by ID.
        
        Args:
            id: Entity ID
            
        Returns:
            T | None: Entity if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def get_all(self, **kwargs) -> list[T]:
        """Get all entities, with optional filtering.
        
        Args:
            **kwargs: Filter parameters
            
        Returns:
            list[T]: List of entities
        """
        pass
    
    @abstractmethod
    async def create(self, entity: T) -> T:
        """Create a new entity.
        
        Args:
            entity: Entity to create
            
        Returns:
            T: Created entity
        """
        pass
    
    @abstractmethod
    async def update(self, id: Any, entity: T) -> T | None:
        """Update an existing entity.
        
        Args:
            id: Entity ID
            entity: Updated entity data
            
        Returns:
            T | None: Updated entity if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def delete(self, id: Any) -> bool:
        """Delete an entity by ID.
        
        Args:
            id: Entity ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        pass 