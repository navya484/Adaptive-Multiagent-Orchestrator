from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# In production, use environment variables. Hardcoded for Phase 2 scaffolding.
DATABASE_URL = "postgresql+asyncpg://admin:adminpassword@localhost:5432/multiagent_db"

engine = create_async_engine(DATABASE_URL, echo=False)

# Session factory for async database operations
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    """Dependency to provide a database session for FastAPI routes."""
    async with AsyncSessionLocal() as session:
        yield session
