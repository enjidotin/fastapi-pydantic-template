from collections.abc import AsyncGenerator, Generator
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.adapters.repositories.sqlalchemy_models import Base
from app.core.domain.item import Item
from app.main import app

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
def test_client() -> Generator[TestClient, None, None]:
    """Create a test client for the FastAPI application."""
    with TestClient(app) as client:
        yield client


@pytest.fixture
async def test_db_engine() -> AsyncGenerator[Any, None]:
    """Create a test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        future=True,
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def test_db_session(test_db_engine: Any) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    # Use async_sessionmaker for better typing support
    async_session = async_sessionmaker(bind=test_db_engine, expire_on_commit=False)

    async with async_session() as session:
        yield session


@pytest.fixture
def sample_item() -> Item:
    """Create a sample item for testing."""
    return Item(
        id=1,
        name="Test Item",
        description="A test item for testing",
        price=99.99,
        is_active=True,
    )
