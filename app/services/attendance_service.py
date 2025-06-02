#!/usr/bin/env python3
# File: services/attendance_service.py
# Author: Oluwatobiloba Light
"""Attendance Services"""


from datetime import date, datetime, time
from typing import Sequence
from uuid import UUID
from app.core.exceptions import GeneralError
from app.models.attendance import (
    Attendance,
    AttendanceClockStatusType,
    AttendanceStatusType,
)
from app.models.user import User
from app.repositories.attendance_repository import AttendanceRepository
from app.schemas.attendance_schema import (
    AttendanceClockStatusTypeSchema,
    AttendanceStatusTypeSchema,
    CreateAttendanceSchema,
)
from app.services.base_service import BaseService
import logging


logger = logging.getLogger(__name__)


class AttendanceService(BaseService):
    def __init__(self, attendance_repository: AttendanceRepository):
        self.attendance_repository = attendance_repository

        super().__init__(attendance_repository)

    async def clock_in(self, user: User) -> Attendance:
        """User attendance clock in"""
        existing = await self.attendance_repository.get_by_user_and_date(
            user.id, date.today()
        )

        if existing:
            raise GeneralError("Already clocked in today.")

        now = datetime.now()
        clock_in_time = now.time()
        clock_in_date = now.date()

        # Reference time: 8:30 AM
        reference_time = time(8, 30)

        if clock_in_time < reference_time:
            clock_in_status = AttendanceClockStatusType.EARLY
        elif clock_in_time == reference_time:
            clock_in_status = AttendanceClockStatusTypeSchema.PRESENT
        else:
            clock_in_status = AttendanceClockStatusTypeSchema.LATE

        attendance = CreateAttendanceSchema(
            user_id=user.id,
            user=user,
            clock_in_date=clock_in_date,
            clock_in_time=clock_in_time,
            clock_in_status=clock_in_status,
        )

        try:
            new_user_attendance = await self.attendance_repository.create(attendance)

            return new_user_attendance
        except Exception as e:
            logger.error(f"An error has occured during clock in {e}")
            raise GeneralError(detail="An error has occured")

    async def clock_out(self, user: User) -> Attendance:
        """User attendance clock out"""

        existing = await self.attendance_repository.get_by_user_and_date(
            user.id, date.today()
        )
        if not existing:
            raise GeneralError("You must clock in before you can clock out.")

        if existing.clock_out_time:
            raise GeneralError("You have already clocked out today.")

        now = datetime.now()
        existing.clock_out_time = now.time()

        clock_in_datetime = datetime.combine(date.today(), existing.clock_in_time)
        clock_out_datetime = datetime.combine(date.today(), existing.clock_out_time)
        total_hours_worked = clock_out_datetime - clock_in_datetime
        total_hours = total_hours_worked.total_seconds() / 3600

        reference_end_time = time(17, 0)
        early_leave_time = time(15, 30)
        status = AttendanceStatusTypeSchema.ACCURATE
        clock_out_status = AttendanceClockStatusTypeSchema.PRESENT

        if clock_out_datetime.time() <= early_leave_time:
            status = AttendanceStatusType.EARLY
            clock_out_status = AttendanceClockStatusType.EARLY
        elif clock_out_datetime.time() >= reference_end_time:
            status = AttendanceStatusType.LATE
            clock_out_status = AttendanceClockStatusType.LATE
        else:
            status = AttendanceStatusType.ACCURATE
            clock_out_status = AttendanceClockStatusType.PRESENT

        try:
            existing.status = status
            existing.clock_out_status = clock_out_status
            existing.total_hours = total_hours
            updated = await self.attendance_repository.update_by_id(
                existing.id,
                existing,
            )
            return updated

        except Exception as e:
            logger.error(f"An error has occured while clocking out: {e}")
            raise GeneralError(detail="An error has occured during clock out.")

    async def get_current_user_attendance_records(
        self, user_id: UUID
    ) -> Sequence[Attendance]:
        """Gets all user attendance records"""
        try:
            return await self.attendance_repository.get_all(user_id)
        except Exception as e:
            logger.error(
                f"Failed to retrieve attendance records of user_id {user_id}: {e}"
            )
            raise GeneralError(
                detail="An error has occured retreiving your attendance records"
            )
