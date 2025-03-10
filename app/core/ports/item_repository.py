from app.core.domain.item import Item
from app.core.ports.repositories import Repository


class ItemRepository(Repository[Item]):
    """Item repository interface.

    This is a specific port for the Item entity in the hexagonal architecture.
    """

    async def find_by_name(self, name: str) -> list[Item]:
        """Find items by name (partial match).

        Args:
            name: Item name to search for

        Returns:
            list[Item]: List of matching items
        """
        pass

    async def find_active_items(self) -> list[Item]:
        """Find all active items.

        Returns:
            list[Item]: List of active items
        """
        pass
