from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Create async engine for PostgreSQL
engine_kwargs = {
    "echo": settings.DEBUG,
    "future": True,
}

if settings.DATABASE_URL and settings.DATABASE_URL.startswith("postgresql"):
    engine_kwargs["pool_size"] = 20
    engine_kwargs["max_overflow"] = 10

engine = create_async_engine(settings.DATABASE_URL, **engine_kwargs)

# Async session maker
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

# Dependency for FastAPI injection
async def get_db() -> AsyncSession:
    """
    Dependency function that yields database sessions.
    Used in FastAPI endpoints to interact with the database.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
