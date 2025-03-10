from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base

# Create the declarative base - this is a class factory
Base = declarative_base()


# Using a more specific type ignore comment to address the Base class issue
class ItemModel(Base):  # type: ignore[misc, valid-type]
    """SQLAlchemy model for items table."""

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
