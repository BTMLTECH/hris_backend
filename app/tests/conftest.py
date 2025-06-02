from contextlib import _AsyncGeneratorContextManager
import os
from os import PathLike
from typing import Any, AsyncGenerator, Callable, Generator
import pytest
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
# from app.adapter.sqlalchemy_adapter import SQLAlchemyAdapter
from app.adapter.sqlalchemy_adapter import SQLAlchemyAdapter
from app.core import Database
from app.core.config import hris_config
from app.adapter.json_adapter import JSONAdapter
from app.main import AppCreator

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/hris_db_dev"


@pytest.fixture
def hris_test_mock():
    """TEST HRIS APP"""
    app_mock = AppCreator()

    return app_mock


@pytest.mark.asyncio
async def test_database_initialization():
    """Test if the database engine initializes correctly."""
    assert hris_test_mock is not None
    db = hris_test_mock().db

    db.create_async_database()

    # assert isinstance(db._engine, AsyncSession)
    assert db._engine is not None
    assert isinstance(db._engine.url.database, str)


@pytest.fixture(scope="session")
async def sqlalchemy_adapter():
    """Provides a fresh SQLAlchemyAdapter for each test."""
    db = hris_test_mock().db
    db.create_async_database()

    async def session_provider():
        async with db.session() as session:
            yield session

    return SQLAlchemyAdapter(session_provider)


@pytest.fixture(scope="function")
def json_adapter(tmp_path):
    """Return an instance of JSONAdapter using a temporary file."""
    print("path", tmp_path)
    test_file = "db.json"
    return JSONAdapter(file_path=str(test_file))
