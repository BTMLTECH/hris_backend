#!/usr/bin/env python3
# File: repositories/user_department_repository.py
# Author: Oluwatobiloba Light
"""User Department Link Repository"""

from datetime import date
from uuid import UUID
from sqlalchemy import select, update
from app.adapter.json_adapter import JSONAdapter
from app.adapter.sqlalchemy_adapter import SQLAlchemyAdapter
from app.models.user_department import UserDepartmentLink
from typing import List, Optional, Sequence, TypeVar, Union
from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import selectinload
import logging


logger = logging.getLogger(__name__)

T = TypeVar("T", bound=UserDepartmentLink)


class UserDepartmentLinkRepository(BaseRepository):
    def __init__(self, db_adapter: Union[JSONAdapter, SQLAlchemyAdapter]):
        self.db_adapter = db_adapter
        self.model = UserDepartmentLink

        super().__init__(db_adapter, UserDepartmentLink)
    
    async def create(self, user_id: UUID, department_id: UUID) -> UserDepartmentLink:
        """Creates a new user-department record in the database"""
        new_user_department = self.model(user_id=user_id, department_id=department_id)
        async with self.session_scope() as session:
            try:
                session.add(new_user_department)
                await session.flush(session,)
                await session.refresh(new_user_department)

                query = select(self.model).where(self.model.id == new_user_department.id)

                result = (await session.execute(query)).scalar_one()

                return result
            except Exception as e:
                raise
    
    async def exists(self, user_id: UUID, department_id: UUID) -> bool:
        statement = select(self.model).where(
            self.model.user_id == user_id,
            self.model.department_id == department_id
        )

        async with self.session_scope() as session:
            try:
                result = (await session.execute(statement)).scalar()

                return result is not None
            except Exception as e:
                raise

    def remove(self, user_id: UUID, department_id: UUID) -> bool:
        statement = select(UserDepartmentLink).where(
            UserDepartmentLink.user_id == user_id,
            UserDepartmentLink.department_id == department_id
        )
        result = self.session.exec(statement).first()
        if result:
            self.session.delete(result)
            self.session.commit()
            return True
        return False

    def get_departments_for_user(self, user_id: UUID) -> List[UserDepartmentLink]:
        statement = select(UserDepartmentLink).where(UserDepartmentLink.user_id == user_id)
        return self.session.exec(statement).all()

    def get_users_for_department(self, department_id: UUID) -> List[UserDepartmentLink]:
        statement = select(UserDepartmentLink).where(UserDepartmentLink.department_id == department_id)
        return self.session.exec(statement).all()