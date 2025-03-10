from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class ItemBase(BaseModel):
    """Base schema for item data."""
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    is_active: bool = True


class ItemCreate(ItemBase):
    """Schema for creating a new item."""
    pass


class ItemUpdate(BaseModel):
    """Schema for updating an item."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    is_active: Optional[bool] = None


class ItemResponse(ItemBase):
    """Schema for item response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ItemListResponse(BaseModel):
    """Schema for a list of items response."""
    items: List[ItemResponse]
    count: int


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    detail: str 