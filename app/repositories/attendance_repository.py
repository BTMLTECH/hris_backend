#!/usr/bin/env python3
# File: repositories/attendance_repository.py
# Author: Oluwatobiloba Light
"""Attendance Repository"""

from datetime import date
from uuid import UUID, uuid4
from sqlalchemy import select, update
from app.adapter.json_adapter import JSONAdapter
from app.adapter.sqlalchemy_adapter import SQLAlchemyAdapter
from app.models.attendance import (
    Attendance,
    AttendanceClockStatusType,
    AttendanceStatusType,
)
from typing import List, Optional, Sequence, TypeVar, Union
from psycopg2 import IntegrityError
from app.core.exceptions import (
    CustomDatabaseError,
    DuplicatedError,
    GeneralError,
    NotFoundError,
)
from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import (
    OperationalError,
    ProgrammingError,
    NoResultFound,
    StatementError,
)
import logging

from app.schemas.attendance_schema import CreateAttendanceSchema

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=Attendance)


class AttendanceRepository(BaseRepository):
    def __init__(self, db_adapter: Union[JSONAdapter, SQLAlchemyAdapter]):
        self.db_adapter = db_adapter
        self.model = Attendance

        super().__init__(db_adapter, Attendance)

    async def create(self, attendance_schema=CreateAttendanceSchema) -> Attendance:
        """Creates user attendance record in the database"""
        user = attendance_schema.user

        async with self.session_scope() as session:
            try:
                clock_in_status = (
                    AttendanceClockStatusType.EARLY
                    if attendance_schema.clock_in_status.name == "EARLY"
                    else (
                        AttendanceClockStatusType.PRESENT
                        if attendance_schema.clock_in_status.name == "PRESENT"
                        else AttendanceClockStatusType.LATE
                    )
                )

                new_attendance = self.model(
                    user=user,
                    clock_in_status=clock_in_status,
                    **attendance_schema.model_dump(
                        exclude_none=True, exclude=["user", "clock_in_status"]
                    )
                )

                session.add(new_attendance)
                await session.flush()
                await session.refresh(new_attendance)

                query_result = (
                    await session.execute(
                        select(self.model)
                        .where(self.model.id == new_attendance.id)
                        .options(selectinload(self.model.user))
                    )
                ).scalar_one()

                new_attendance = query_result
                return new_attendance
            except Exception as e:
                raise

    async def get_by_user_and_date(
        self, user_id: UUID, _date: date
    ) -> Optional[Attendance]:
        async with self.session_scope() as session:
            try:
                result = await session.execute(
                    select(self.model)
                    .where(
                        self.model.user_id == user_id, self.model.clock_in_date == _date
                    )
                    .options(selectinload(self.model.user))
                )
                return result.scalars().first()
            except Exception:
                raise

    async def get_user_attendance(self, user_id: UUID) -> List[Attendance]:
        async with self.session_scope() as session:
            result = await session.execute(
                select(self.model).where(self.model.user_id == user_id)
            )
            return result.scalars().all()

    async def update_by_id(self, id: UUID, attendance: Attendance) -> Attendance:
        """Update user attendance record"""
        async with self.session_scope() as session:
            try:
                query = (
                    update(self.model)
                    .where(self.model.id == id)
                    .values(
                        {
                            "status": attendance.status,
                            "clock_out_status": attendance.clock_out_status,
                            **attendance.model_dump(
                                exclude=["status", "clock_out_status"]
                            ),
                        }
                    )
                    .execution_options(synchronize_session="fetch")
                )

                result = await session.execute(query)

                query = (
                    select(self.model)
                    .where(self.model.id == id)
                    # .options(selectinload(self.model.user))
                )

                updated_record = (await session.execute(query)).scalar_one()

                if result.rowcount < 1:
                    return updated_record

                return updated_record
            except:
                raise

    async def get_all(self, user_id: UUID) -> Sequence[Attendance]:
        """Get all attendance records of a user from the database"""
        async with self.session_scope() as session:
            try:
                query = (
                    select(self.model)
                    .where(self.model.user_id == user_id)
                    # .options(selectinload(self.model.user))
                )

                result = (await session.execute(query)).scalars().all()

                return result
            except Exception:
                raise
