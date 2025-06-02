import asyncio
from contextlib import asynccontextmanager
import pytest
from app.adapter.sqlalchemy_adapter import SQLAlchemyAdapter
from app.core.exceptions import DuplicatedError
from app.main import AppCreator
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import CreateUser
from app.core.database import Base


@pytest.fixture(scope="session")
def event_loop():
    """Create a new event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def setup_teardown():
    """Setup and teardown for each test"""
    app = AppCreator()
    db = app.db
    await db.create_async_database()
    yield
    # Clean up the database after each test
    async with db._sessionmaker() as session:
        for table in reversed(db.session):
            await session.execute(table.delete())
        await session.commit()


@pytest.fixture
async def hris_db_session():
    """TEST HRIS APP"""
    app = AppCreator()
    db = app.db

    @asynccontextmanager
    async def session_provider():
        async with db._sessionmaker() as session:
            try:
                yield session
            finally:
                await session.close()

    return session_provider


@pytest.mark.asyncio
async def test_user_create_retrieve(hris_db_session):
    """Test adding and retrieving data using SQLAlchemyAdapter."""
    user_repo = UserRepository(
        db_adapter=SQLAlchemyAdapter(await hris_db_session))

    new_user = CreateUser(first_name="Oluwatobiloba", middle_name="John", last_name="Agunloye",
                          email="oluwatobilobagunloye@gmail.com", password="123456", staff_id=484, office_email="oluwatobi.agunloye@btmlimited.net")

    await user_repo.create(new_user)

    fetched_user = await user_repo.get_by_email("oluwatobilobagunloye@gmail.com")

    assert fetched_user is not None
    assert fetched_user.email == "oluwatobilobagunloye@gmail.com"


@pytest.mark.asyncio
async def test_user_raise_error(hris_db_session):
    """Test user create and raise duplicate error."""
    user_repo = UserRepository(
        db_adapter=SQLAlchemyAdapter(await hris_db_session))

    new_user = CreateUser(first_name="Oluwatobiloba", middle_name="John", last_name="Agunloye",
                          email="oluwatobilobagunloye1@gmail.com", password="123456", staff_id=485, office_email="oluwatobi.agunloye1@btmlimited.net")

    await user_repo.create(new_user)

    try:
        await user_repo.create(new_user)
        pytest.fail("An account with that email address exists!")
    except DuplicatedError as error:
        assert error.status_code == 400
        assert "An account with that email address exists!" in str(
            error.detail)
