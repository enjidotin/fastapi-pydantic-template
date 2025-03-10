from datetime import datetime

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    """Base schema for item data."""
    name: str
    description: str | None = None
    price: float = Field(gt=0)
    is_active: bool = True


class ItemCreate(ItemBase):
    """Schema for creating a new item."""
    pass


class ItemUpdate(BaseModel):
    """Schema for updating an item."""
    name: str | None = None
    description: str | None = None
    price: float | None = Field(default=None, gt=0)
    is_active: bool | None = None


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
    items: list[ItemResponse]
    count: int


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    detail: str 