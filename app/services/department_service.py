#!/usr/bin/env python3
# File: services/department_service.py
# Author: Oluwatobiloba Light
"""Department Services"""


from typing import List, Optional
from uuid import UUID
from sqlalchemy import Sequence
from app.models.department import Department
from app.models.user_department import UserDepartmentLink
from app.repositories.department_repository import DepartmentRepository
from app.repositories.user_department_repository import UserDepartmentLinkRepository
from app.schemas.department_schema import CreateDepartmentSchema, UpdateDepartmentSchema
from app.core.exceptions import GeneralError, NotFoundError
import logging
from sqlalchemy.exc import SQLAlchemyError

from app.services.base_service import BaseService


logger = logging.getLogger(__name__)


class DepartmentService(BaseService):
    def __init__(
        self,
        department_repository: DepartmentRepository,
        user_department_repository: UserDepartmentLinkRepository,
    ):
        self.department_repository = department_repository
        self.user_department_repository = user_department_repository

    async def create_department(self, schema: CreateDepartmentSchema) -> Department:
        logger.info(f"Creating a new department...")
        try:
            department = await self.department_repository.create(schema)

            logger.info(f"Department created: {department.name}")
            return department
        except SQLAlchemyError as e:
            orig = getattr(e, "orig", None)
            if orig:
                db_error = str(orig)
                detail = getattr(orig, "detail", None)
                message = f"{detail}" if detail else db_error
            else:
                message = str(e)

            logger.error(f"Database error during department creation: {message}")
            raise GeneralError(
                detail="An error has occured while creating a department"
            )

    async def assign_team_lead(self, team_lead_id: str, department_id: str):
        """Assign a team lead to a department"""
        logger.info("Assigning team lead...")
        try:
            department = await self.department_repository.assign_team_lead(
                team_lead_id, department_id
            )

            return department
        except SQLAlchemyError as e:
            orig = getattr(e, "orig", None)
            if orig:
                db_error = str(orig)
                detail = getattr(orig, "detail", None)
                message = f"{detail}" if detail else db_error
            else:
                message = str(e)

            logger.error(f"Database error while assigning team lead: {message}")
            raise GeneralError(detail="Unable to assign User ID")

    async def assign_team_member(self, user_id: str, department_id: str):
        """Assign a team member to a department"""

        def validate_uid(value: str):
            try:
                return UUID(value)
            except (TypeError, ValueError):
                raise GeneralError(detail=f"Invalid ID")

        logger.info("Assigning team member...")

        try:
            department_uid = validate_uid(department_id)

            user_uid = validate_uid(user_id)

            user_department = await self.user_department_repository.exists(
                user_uid, department_uid
            )

            if not user_department:
                logger.info(f"Adding user to department...")
                try:
                    await self.user_department_repository.create(
                        user_id, department_uid
                    )

                    logger.info(f"User has been added to department successfully")

                    return await self.department_repository.get_by_id(department_uid)
                except Exception as e:
                    logger.error(f"Database error while assigning team member")
                    raise GeneralError(
                        detail="An error occured while adding user to department"
                    )

            logger.info(f"User has been added to department successfully")
            return await self.department_repository.get_by_id(department_uid)

        except SQLAlchemyError as e:
            orig = getattr(e, "orig", None)
            if orig:
                db_error = str(orig)
                detail = getattr(orig, "detail", None)
                message = f"{detail}" if detail else db_error
            else:
                message = str(e)

            logger.error(f"Database error while assigning team member: {message}")

    async def get_all_departments(self) -> Sequence[Department]:
        """Get all departments"""
        try:
            departments = await self.department_repository.get_all()

            return departments
        except SQLAlchemyError as e:
            orig = getattr(e, "orig", None)
            if orig:
                db_error = str(orig)
                detail = getattr(orig, "detail", None)
                message = f"{detail}" if detail else db_error
            else:
                message = str(e)

            logger.error(f"Database error while getting departments: {message}")
            raise GeneralError(
                detail="An error has occured while getting list of departments"
            )

    async def get_department_by_id(self, id: str) -> Optional[Department]:
        """Get a department by ID"""
        try:
            department = await self.department_repository.get_by_id(id)

            return department
        except SQLAlchemyError as e:
            orig = getattr(e, "orig", None)
            if orig:
                db_error = str(orig)
                detail = getattr(orig, "detail", None)
                message = f"{detail}" if detail else db_error
            else:
                message = str(e)

            logger.error(f"Database error while getting departments: {message}")
            raise GeneralError(
                detail="An error has occured while getting list of departments"
            )

    async def update_department_by_id(self, id: str, department: UpdateDepartmentSchema):
        """Update a department by ID"""
        from uuid import UUID

        try:
            department_uid = UUID(id)
        except (TypeError, ValueError):
            raise GeneralError(detail="Department ID is invalid", status_code=400)
        
        try:
            department_data = await self.get_department_by_id(id)

            if not department_data or department_data is None:
                raise NotFoundError(detail="Department not found or doesn't exist")
            
            return await self.department_repository.update_by_id(department_uid, department)
        except Exception as e:
            logger.error(f"An error has occured while updating department {e}")
            raise GeneralError(detail="Could not update department")