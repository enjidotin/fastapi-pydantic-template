import re
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.adapters.repositories.sqlalchemy_models import Base
from app.core.config import settings

# Handle both standard PostgreSQL URLs and asyncpg URLs
db_url = settings.DATABASE_URL
if db_url.startswith("postgresql://") and not db_url.startswith("postgresql+"):
    # Convert to asyncpg URL for better async performance
    db_url = re.sub(r"^postgresql://", "postgresql+asyncpg://", db_url)

# Create async engine
engine = create_async_engine(
    db_url,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,  # Enable connection health checks
)

# Create async session factory
# Use async_sessionmaker for better typing support with AsyncSession
async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session.

    Yields:
        AsyncSession: Database session
    """
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize the database by creating all tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
