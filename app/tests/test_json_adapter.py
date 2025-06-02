from uuid import uuid4
import pytest

from app.core.exceptions import DuplicatedError
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import CreateUser


@pytest.mark.asyncio
async def test_create_user(json_adapter):
    """Test adding data using JSONAdapter."""
    user_repo = UserRepository(json_adapter)

    new_user = CreateUser(first_name="Oluwatobiloba", middle_name="John", last_name="Agunloye",
                          email="oluwatobilobagunloye@gmail.com", password="123456", staff_id=484, office_email="oluwatobi.agunloye@btmlimited.net")

    user = await user_repo.create(new_user)

    assert user is not None
    assert user.first_name == "Oluwatobiloba"
    assert user.last_name == "Agunloye"
    assert user.email == "oluwatobilobagunloye@gmail.com"


@pytest.mark.asyncio
async def test_create_user_staff_id_duplicate(json_adapter):
    """Test adding a duplicate data using JSONAdapter."""
    user_repo = UserRepository(json_adapter)

    new_user = CreateUser(first_name="Oluwatobiloba", middle_name="John", last_name="Agunloye",
                          email="oluwatobilobagunloye@gmail.com", password="123456", staff_id=484, office_email="oluwatobi.agunloye@btmlimited.net")

    with pytest.raises(DuplicatedError) as excinfo:
        user = await user_repo.create(new_user)

    assert str(excinfo.value) == "Staff ID is a duplicate!"


@pytest.mark.asyncio
async def test_create_user_email_duplicate(json_adapter):
    """Test adding a duplicate data using JSONAdapter."""
    user_repo = UserRepository(json_adapter)

    new_user = CreateUser(first_name="Oluwatobiloba", middle_name="John", last_name="Agunloye",
                          email="oluwatobilobagunloye@gmail.com", password="123456", staff_id=485, office_email="oluwatobi.agunloye@btmlimited.net")

    with pytest.raises(DuplicatedError) as excinfo:
        user = await user_repo.create(new_user)

    assert str(excinfo.value) == "Email is a duplicate!"
