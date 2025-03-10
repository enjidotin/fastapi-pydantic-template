from datetime import datetime

from pydantic import BaseModel, Field


class BaseDomainModel(BaseModel):
    """Base domain model with common fields and functionality."""
    id: int | None = None
    created_at: datetime | None = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default_factory=datetime.now)
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True  # Allow ORM model -> Pydantic model conversion 