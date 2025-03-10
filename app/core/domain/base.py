from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class BaseDomainModel(BaseModel):
    """Base domain model with common fields and functionality."""
    id: Optional[int] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True  # Allow ORM model -> Pydantic model conversion 