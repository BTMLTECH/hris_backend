#!/usr/bin/env python3
# File: app/services/user_service.py
# Author: Oluwatobiloba Light
"""User Services"""


from typing import List, Optional, Sequence, Union
from uuid import UUID
from app.core.exceptions import DuplicatedError, GeneralError, NotFoundError
from app.models.employment_type import EmploymentType
from app.models.permission import Permission
from app.models.role import Role
from app.models.user import User
from app.repositories.department_repository import DepartmentRepository
from app.repositories.permission_repository import PermissionRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import (
    CreateUserSchema,
    UserSignUpSchema,
)
from app.schemas.user_schema import CreateEmploymentTypeSchema, UpdateEmploymentTypeSchema, UserUpdateSchema
from app.services.base_service import BaseService
import logging
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


class UserService(BaseService):
    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository,
        permission_repository: PermissionRepository,
        department_repository: DepartmentRepository,
    ):
        self.user_repository = user_repository
        self.role_repository = role_repository
        self.permission_repository = permission_repository
        self.department_repository = department_repository

        super().__init__(user_repository)

    async def create_user(self, user_data: UserSignUpSchema) -> Union[User, None]:
        """Creates a new user on HRIS"""
        try:
            logger.info("Creating user with email: %s", user_data.email)

            existing_user = await self.user_repository.get_by_email(user_data.email)

            if existing_user:
                raise GeneralError(
                    detail="User with this email already exists.", status_code=400
                )

            role = await self.role_repository.get_by_name(user_data.user_role.lower())

            if not role:
                raise NotFoundError(f"Role {user_data.user_role} not found.")

            user_data.role_id = role.id
            user_data.role = role

            permissions = (
                [
                    await self.permission_repository.get_by_name(permission.lower())
                    for permission in user_data.user_permissions
                ]
                if user_data.user_permissions and len(user_data.user_permissions) > 0
                else []
            )

            permissions = [
                permission for permission in permissions if permission is not None
            ]

            user_data.permissions = permissions

            new_user = await self.user_repository.create(user_data)
            logger.info("Account created!")

            return new_user
        except SQLAlchemyError as e:
            orig = getattr(e, "orig", None)
            if orig:
                db_error = str(orig)
                detail = getattr(orig, "detail", None)
                message = f"{detail}" if detail else db_error
            else:
                message = str(e)

            logger.error(f"Database error during account creation: {message}")
            raise GeneralError(detail="An error has occured")

    async def add_emplyoment_type(
        self, employment_type_info: CreateEmploymentTypeSchema
    ) -> EmploymentType:
        """Crate an employment type"""
        try:
            return await self.user_repository.create_employment_type(
                employment_type_info
            )
        except SQLAlchemyError as e:
            orig = getattr(e, "orig", None)
            if orig:
                db_error = str(orig)
                detail = getattr(orig, "detail", None)
                message = f"{detail}" if detail else db_error
            else:
                message = str(e)

            logger.error(f"Database error during creation: {message}")
            raise GeneralError(detail="An error has occured")

    async def get_employment_types(self):
        """Get all employment types"""
        try:
            return await self.user_repository.get_all_employment_types()
        except Exception as e:
            raise GeneralError(detail=str(e))

    async def update_employment_type(self, id: str, employment_type_data: UpdateEmploymentTypeSchema):
        """Update an employment type by ID"""
        from uuid import UUID

        try:
            employmt_type_uid = UUID(id)
        except (TypeError, ValueError):
            raise GeneralError(detail="Bank ID is invalid", status_code=400)
        
        try:
            employment_type_data = await self.user_repository.get_employment_type_by_id(id)

            if not employment_type_data or employment_type_data is None:
                raise NotFoundError(detail="Bank not found or doesn't exist")
            
            return await self.user_repository.update_employment_type_by_id(employmt_type_uid, employment_type_data)
        except Exception as e:
            logger.error(f"An error has occured while updating bank: {e}")
            raise GeneralError(detail="Could not update Bank")
    
    async def delete_employment_type_by_id(self, id: str):
        """Delete a bank by ID"""
        from uuid import UUID

        try:
            employment_type_uid = UUID(id)
        except (TypeError, ValueError):
            raise GeneralError(detail="Bank ID is invalid", status_code=400)
        
        try:
            bank_data = await self.user_repository.get_employment_type_by_id(id)

            if not bank_data or bank_data is None:
                raise NotFoundError(detail="Bank not found or doesn't exist")
            
            return await self.user_repository.delete_employment_type_by_id(employment_type_uid)
        except Exception as e:
            logger.error(f"An error has occured while deleting bank: {e}")
            raise GeneralError(detail="Could not delete Bank")

    async def get_by_id(self, id: str) -> Optional[User]:
        """Get a user by their ID"""
        user_uid: UUID

        try:
            user_uid = UUID(id)
        except (TypeError, ValueError):
            raise GeneralError(detail="User ID is invalid", status_code=400)

        try:
            return await self.user_repository.get_by_id(user_uid)
        except Exception as e:
            raise GeneralError(detail=str(e))

    async def get_all(self) -> Sequence[User]:
        """Get all users on HRIS"""
        try:
            return await self.user_repository.get_all()
        except Exception as e:
            raise GeneralError(detail=str(e))

    async def update_user_profile(self, user: User, user_info: CreateUserSchema):
        """Update a user profile"""
        print(user_info)
        return None

    async def edit_employee_profile(self, user_id: str, user_info: UserUpdateSchema):
        """Edit an employee's profile by admin"""
        from uuid import UUID

        try:
            user_uid = UUID(user_id)
        except (TypeError, ValueError):
            raise GeneralError(detail="User ID is invalid", status_code=400)

        # Fetch the user to ensure they exist
        user = await self.user_repository.get_by_id(user_uid)
        if not user:
            raise GeneralError(detail="User not found", status_code=404)

        # Update the user profile
        updated_user = await self.user_repository.update_by_id(
            user_uid, user_info
        )
        return updated_user

    async def delete_by_id(self, id: str) -> Optional[User]:
        """Delete a user by their ID"""
        user_uid: UUID

        try:
            user_uid = UUID(id)
        except (TypeError, ValueError):
            raise GeneralError(detail="User ID is invalid", status_code=400)

        try:
            return await self.user_repository.delete_by_id(user_uid)
        except Exception as e:
            raise GeneralError(detail=str(e))

    async def activate_employee(self, id: str):
        """Activates an employee using their ID"""
        user_uid: UUID

        try:
            user_uid = UUID(id)
        except (TypeError, ValueError):
            raise GeneralError(detail="User ID is invalid", status_code=400)

        try:
            return await self.user_repository.activate_user(user_uid)
        except Exception as e:
            raise GeneralError(detail=str(e))

    async def deactivate_employee(self, id: str):
        """Deactivates an employee using their ID"""
        user_uid: UUID

        try:
            user_uid = UUID(id)
        except (TypeError, ValueError):
            raise GeneralError(detail="User ID is invalid", status_code=400)

        try:
            return await self.user_repository.deactivate_user(user_uid)
        except Exception as e:
            raise GeneralError(detail=str(e))
