import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.adapter.sqlalchemy_adapter import SQLAlchemyAdapter
from app.core.database import Database, Base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import AppCreator

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/hris_db_dev"


@pytest.fixture
def hris_test_mock():
    """TEST HRIS APP"""
    app_mock = AppCreator()

    return app_mock


@pytest.mark.asyncio
async def test_database_initialization(hris_test_mock):
    """Test if the database engine initializes correctly."""
    assert hris_test_mock is not None
    db = hris_test_mock.db

    db.create_async_database()

    # assert isinstance(db._engine, AsyncSession)
    assert db._engine is not None
    assert isinstance(db._engine.url.database, str)


@pytest.fixture(scope="function")
async def sqlalchemy_adapter(hris_test_mock):
    """Provides a fresh SQLAlchemyAdapter for each test."""
    db = hris_test_mock.db
    db.create_async_database()

    async def session_provider():
        async with db.session() as session:
            yield session

    return SQLAlchemyAdapter(session_provider)
