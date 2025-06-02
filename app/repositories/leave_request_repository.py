#!/usr/bin/env python3
# File: repositories/leave_request_repository.py
# Author: Oluwatobiloba Light
"""Leave Request Repository"""

from datetime import date
from uuid import UUID
from sqlalchemy import select, update
from app.adapter.json_adapter import JSONAdapter
from app.adapter.sqlalchemy_adapter import SQLAlchemyAdapter
from app.models.leave_request import (
    LeaveRequest,
    LeaveRequestType,
)
from typing import List, Optional, Sequence, TypeVar, Union
from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import selectinload
import logging

from app.schemas.leave_schema import CreateLeaveRequestSchema

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=LeaveRequest)


class LeaveRequestRepository(BaseRepository):
    def __init__(self, db_adapter: Union[JSONAdapter, SQLAlchemyAdapter]):
        self.db_adapter = db_adapter
        self.model = LeaveRequest

        super().__init__(db_adapter, LeaveRequest)

    async def create(self, schema: CreateLeaveRequestSchema) -> LeaveRequest:
        """Creates a new leave request record in the database"""
        async with self.session_scope() as session:
            try:
                query = self.model(status=LeaveRequestType.PENDING, **schema.model_dump(exclude=["status"]))

                self.db_adapter.add(session, query)
                await self.db_adapter.flush(session)
                await self.db_adapter.refresh(session, query)

                query_result = (
                    select(self.model)
                    .where(self.model.id == query.id)
                    .options(selectinload(self.model.leave_approvers), selectinload(self.model.leave_relievers), selectinload(self.model.user))
                )

                query = (await session.execute(query_result)).scalar_one()

                return query
            except:
                raise

    async def get_by_id(self, id: UUID) -> Optional[LeaveRequest]:
        async with self.session_scope() as session:
            stmt = select(self.model).where(self.model.id == id)
            result = await session.execute(stmt)
            return result.scalars().first()

    async def get_all_for_user(self, user_id: UUID) -> List[LeaveRequest]:
        async with self.session_scope() as session:
            stmt = select(self.model).where(self.model.user_id == user_id)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def update_by_id(self, id: UUID, instance: LeaveRequest) -> Optional[LeaveRequest]:
        async with self.session_scope() as session:
            session.add(instance)
            await session.flush()
            await session.refresh(instance)
            return instance

    async def get_all(self) -> List[LeaveRequest]:
        async with self.session_scope() as session:
            stmt = select(self.model)
            result = await session.execute(stmt)
            return result.scalars().all()