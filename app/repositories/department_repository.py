#!/usr/bin/env python3
# File: repositories/department_repository.py
# Author: Oluwatobiloba Light
"""Department Repository"""

from datetime import date
from uuid import UUID
from sqlalchemy import select, update, func
from app.adapter.json_adapter import JSONAdapter
from app.adapter.sqlalchemy_adapter import SQLAlchemyAdapter
from app.models.department import Department
from typing import List, Optional, Sequence, TypeVar, Union
from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import selectinload
import logging
from sqlalchemy.exc import IntegrityError
from app.schemas.department_schema import CreateDepartmentSchema

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=Department)


class DepartmentRepository(BaseRepository):
    def __init__(self, db_adapter: Union[JSONAdapter, SQLAlchemyAdapter]):
        self.db_adapter = db_adapter
        self.model = Department

        super().__init__(db_adapter, Department)

    async def create(self, department_schema=CreateDepartmentSchema) -> Department:
        """Creates a new department record in the database"""
        async with self.session_scope() as session:
            try:
                new_department = self.model(**department_schema.model_dump())

                session.add(new_department)
                await session.flush(session)
                await session.refresh(new_department)

                query = (
                    select(self.model)
                    .where(self.model.id == new_department.id)
                    .options(
                        selectinload(self.model.team_lead),
                        selectinload(self.model.team_members),
                    )
                )

                new_department = (await session.execute(query)).scalar_one()

                return new_department
            except IntegrityError as e:
                logger.error("Integrity error during user creation: %s", e)
                raise e
            except Exception as e:
                logger.error("Unexpected error during user creation: %s", e)
                raise e

    async def get_by_id(self, id: UUID) -> Optional[Department]:
        """Get a department record by id from the database"""
        async with self.session_scope() as session:
            from app.models.user import User

            try:
                query = (
                    select(self.model)
                    .where(self.model.id == id)
                    .options(
                        selectinload(self.model.team_members),
                        selectinload(self.model.team_lead),
                        selectinload(self.model.team_members).selectinload(
                            User.permissions
                        ),
                        selectinload(self.model.team_members).selectinload(User.role),
                        selectinload(self.model.team_members).selectinload(
                            User.employment_type
                        ),
                        selectinload(self.model.team_members).selectinload(
                            User.pension
                        ),
                        selectinload(self.model.team_members).selectinload(User.bank),
                        selectinload(self.model.team_members).selectinload(
                            User.payroll_class
                        ),
                        selectinload(self.model.team_members).selectinload(
                            User.department
                        ),
                        selectinload(self.model.team_members).selectinload(
                            User.leave_requests
                        ),
                        selectinload(self.model.team_members).selectinload(
                            User.attendance
                        ),
                        selectinload(self.model.team_members).selectinload(
                            User.next_of_kin
                        ),
                        selectinload(self.model.team_lead).selectinload(
                            User.permissions
                        ),
                        selectinload(self.model.team_lead).selectinload(User.role),
                        selectinload(self.model.team_lead).selectinload(
                            User.employment_type
                        ),
                        selectinload(self.model.team_lead).selectinload(User.pension),
                        selectinload(self.model.team_lead).selectinload(User.bank),
                        selectinload(self.model.team_lead).selectinload(
                            User.payroll_class
                        ),
                        selectinload(self.model.team_lead).selectinload(
                            User.department
                        ),
                        selectinload(self.model.team_lead).selectinload(
                            User.leave_requests
                        ),
                        selectinload(self.model.team_lead).selectinload(
                            User.attendance
                        ),
                        selectinload(self.model.team_lead).selectinload(
                            User.next_of_kin
                        ),
                    )
                )

                result = (await session.execute(query)).scalar_one_or_none()

                return result
            except IntegrityError as e:
                logger.error("Integrity error: %s", e)
                raise e
            except Exception as e:
                logger.error("Unexpected error: %s", e)
                raise e

    async def get_by_name(self, name: str) -> Optional[Department]:
        async with self.session_scope() as session:
            from app.models.user import User

            try:
                query = (
                    select(self.model)
                    .where(func.lower(self.model.name) == name.lower())
                    .options(
                        # selectinload(self.model.team_members),
                        # selectinload(self.model.team_lead),
                        selectinload(self.model.team_members).selectinload(
                            User.permissions
                        ),
                        selectinload(self.model.team_members).selectinload(User.role),
                        selectinload(self.model.team_members).selectinload(
                            User.employment_type
                        ),
                        selectinload(self.model.team_members).selectinload(
                            User.pension
                        ),
                        selectinload(self.model.team_members).selectinload(User.bank),
                        selectinload(self.model.team_members).selectinload(
                            User.payroll_class
                        ),
                        selectinload(self.model.team_members).selectinload(
                            User.department
                        ),
                        selectinload(self.model.team_members).selectinload(
                            User.leave_requests
                        ),
                        selectinload(self.model.team_members).selectinload(
                            User.attendance
                        ),
                        selectinload(self.model.team_members).selectinload(
                            User.next_of_kin
                        ),
                        selectinload(self.model.team_lead).selectinload(
                            User.permissions
                        ),
                        selectinload(self.model.team_lead).selectinload(User.role),
                        selectinload(self.model.team_lead).selectinload(
                            User.employment_type
                        ),
                        selectinload(self.model.team_lead).selectinload(User.pension),
                        selectinload(self.model.team_lead).selectinload(User.bank),
                        selectinload(self.model.team_lead).selectinload(
                            User.payroll_class
                        ),
                        selectinload(self.model.team_lead).selectinload(
                            User.department
                        ),
                        selectinload(self.model.team_lead).selectinload(
                            User.leave_requests
                        ),
                        selectinload(self.model.team_lead).selectinload(
                            User.attendance
                        ),
                        selectinload(self.model.team_lead).selectinload(
                            User.next_of_kin
                        ),
                    )
                )

                result = (await session.execute(query)).scalar_one_or_none()

                return result
            except IntegrityError as e:
                logger.error("Integrity error: %s", e)
                raise e
            except Exception as e:
                logger.error("Unexpected error: %s", e)
                raise e

    async def get_all(self) -> Sequence[Department]:
        """Get all department records from the database"""
        async with self.session_scope() as session:
            from app.models.user import User

            try:
                query = select(self.model).options(
                    # selectinload(self.model.team_members),
                    # selectinload(self.model.team_lead),
                    selectinload(self.model.team_members).selectinload(
                        User.permissions
                    ),
                    selectinload(self.model.team_members).selectinload(User.role),
                    selectinload(self.model.team_members).selectinload(
                        User.employment_type
                    ),
                    selectinload(self.model.team_members).selectinload(User.pension),
                    selectinload(self.model.team_members).selectinload(User.bank),
                    selectinload(self.model.team_members).selectinload(
                        User.payroll_class
                    ),
                    selectinload(self.model.team_members).selectinload(User.department),
                    selectinload(self.model.team_members).selectinload(
                        User.leave_requests
                    ),
                    selectinload(self.model.team_members).selectinload(User.attendance),
                    selectinload(self.model.team_members).selectinload(
                        User.next_of_kin
                    ),
                    selectinload(self.model.team_lead).selectinload(User.permissions),
                    selectinload(self.model.team_lead).selectinload(User.role),
                    selectinload(self.model.team_lead).selectinload(
                        User.employment_type
                    ),
                    selectinload(self.model.team_lead).selectinload(User.pension),
                    selectinload(self.model.team_lead).selectinload(User.bank),
                    selectinload(self.model.team_lead).selectinload(User.payroll_class),
                    selectinload(self.model.team_lead).selectinload(User.department),
                    selectinload(self.model.team_lead).selectinload(
                        User.leave_requests
                    ),
                    selectinload(self.model.team_lead).selectinload(User.attendance),
                    selectinload(self.model.team_lead).selectinload(User.next_of_kin),
                )

                result = (await session.execute(query)).scalars().all()

                return result
            except Exception as e:
                raise e

    async def assign_team_lead(
        self, team_lead_id: UUID, department_id: UUID
    ) -> Optional[Department]:
        """Assign a team lead to a department record in the database"""
        async with self.session_scope() as session:
            try:
                query = (
                    update(self.model)
                    .where(self.model.id == department_id)
                    .values({"team_lead_id": team_lead_id})
                    .execution_options(synchronize_session="fetch")
                )

                result = await session.execute(query)

                q = (
                    select(self.model)
                    .where(self.model.id == department_id)
                    .options(
                        selectinload(self.model.team_lead),
                        selectinload(self.model.team_members),
                    )
                )

                updated_record = (await session.execute(q)).scalar_one_or_none()

                if result.rowcount < 1:
                    return updated_record

                return updated_record
            except Exception as e:
                raise

    async def assign_team_member(
        self, team_members: UUID, department_id: UUID
    ) -> Optional[Department]:
        """Assign a team member to a department record in the database"""
        async with self.session_scope() as session:
            try:
                query = (
                    update(self.model)
                    .where(self.model.id == department_id)
                    .values({"team_lead_id": team_lead_id})
                    .execution_options(synchronize_session="fetch")
                )

                result = await session.execute(query)

                q = (
                    select(self.model)
                    .where(self.model.id == department_id)
                    .options(
                        selectinload(self.model.team_lead),
                        selectinload(self.model.team_members),
                    )
                )

                updated_record = (await session.execute(q)).scalar_one_or_none()

                if result.rowcount < 1:
                    return updated_record

                return updated_record
            except Exception as e:
                raise
