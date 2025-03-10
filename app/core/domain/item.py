
from pydantic import Field

from app.core.domain.base import BaseDomainModel


class Item(BaseDomainModel):
    """Item domain model."""
    name: str
    description: str | None = None
    price: float = Field(gt=0)
    is_active: bool = True
    
    def apply_discount(self, discount_percent: float) -> float:
        """Apply a discount to the item price.
        
        Args:
            discount_percent: Discount percentage (0-100)
            
        Returns:
            float: Discounted price
        """
        if not 0 <= discount_percent <= 100:
            raise ValueError("Discount must be between 0 and 100")
        
        discount_factor = 1 - (discount_percent / 100)
        return self.price * discount_factor 