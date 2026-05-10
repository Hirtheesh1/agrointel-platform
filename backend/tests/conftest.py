import pytest
import asyncio
from typing import AsyncGenerator
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import get_db, Base
from app.core.config import settings
from app.models.farm import Farm
import uuid

# Use an in-memory SQLite database for testing to ensure isolation and speed
# Note: SQLite async support requires aiosqlite, which is installed.
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(autouse=True)
async def setup_database():
    """
    Creates and drops all tables before and after each test.
    This ensures a clean state for every test.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provides a database session for testing repository functions directly."""
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture
def client() -> TestClient:
    """Provides a TestClient for testing FastAPI endpoints."""
    return TestClient(app)

@pytest.fixture
async def sample_tamil_nadu_farm(db_session: AsyncSession):
    """Creates a sample farm in Tamil Nadu for testing."""
    farm = Farm(
        id=uuid.uuid4(),
        farm_name="Coimbatore Test Farm",
        latitude=11.0168,
        longitude=76.9558,
        farm_size=5.5
    )
    db_session.add(farm)
    await db_session.commit()
    await db_session.refresh(farm)
    return farm
