#!/usr/bin/env python3
# File: repositories/supervisor_repository.py
# Author: Oluwatobiloba Light
"""Leave Request Repository"""

from datetime import date
from uuid import UUID
from sqlalchemy import select, update
from app.adapter.json_adapter import JSONAdapter
from app.adapter.sqlalchemy_adapter import SQLAlchemyAdapter
from app.models.user_supervisor import UserSupervisor
from typing import List, Optional, Sequence, TypeVar, Union
from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import selectinload
import logging


logger = logging.getLogger(__name__)

T = TypeVar("T", bound=UserSupervisor)


class UserSupervisorRepository(BaseRepository):
    def __init__(self, db_adapter: Union[JSONAdapter, SQLAlchemyAdapter]):
        self.db_adapter = db_adapter
        self.model = UserSupervisor

        super().__init__(db_adapter, UserSupervisor)

    async def get_supervisors_for_user(self, user_id: UUID):
        async with self.session_scope() as session:
            stmt = select(self.model).where(self.model.user_id == user_id)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_subordinates_for_user(self, user_id: UUID):
        async with self.session_scope() as session:
            stmt = select(self.model).where(self.model.user_id == user_id)
            result = await session.execute(stmt)
            return result.scalars().all()
