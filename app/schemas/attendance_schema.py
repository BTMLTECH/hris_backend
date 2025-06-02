#!/usr/bin/env python3
# File: app/schemas/attendance_schema.py
# Author: Oluwatobiloba Light
"""Attendance Schema"""


from datetime import date, datetime, time
from enum import Enum
from typing import List, Literal, Optional, Union
from uuid import UUID
from pydantic import BaseModel, EmailStr

from app.models.attendance import AttendanceClockStatusType
from app.models.next_of_kin import NextOfKin
from app.models.permission import Permission
from app.models.role import Role
from app.models.user import User
from app.schemas.base_schema import ModelBaseInfo


class AttendanceStatusTypeSchema(Enum):
    ACCURATE = "ACCURATE"
    EARLY = "EARLY"
    LATE = "LATE"


class AttendanceClockStatusTypeSchema(Enum):
    EARLY = "EARLY"
    PRESENT = "PRESENT"
    LATE = "LATE"


class AttendanceSchema(ModelBaseInfo):
    status: Optional[AttendanceStatusTypeSchema] 

    clock_in_date: Optional[date]

    clock_in_time: Optional[time]

    clock_out_time: Optional[time]

    clock_in_status: AttendanceClockStatusType

    clock_out_status: Optional[AttendanceClockStatusType]

    total_hours: Optional[float]

    user_id: Optional[UUID]

    # user: Optional[User] = None


class CreateAttendanceSchema(BaseModel):
    clock_in_date: Optional[date]

    clock_in_time: Optional[time]

    user: User

    user_id: UUID

    clock_in_status: AttendanceClockStatusTypeSchema


class UpdateAttendanceSchema(BaseModel):
    clock_in_time: Optional[time]

    user: User

    user_id: UUID

    status: AttendanceStatusTypeSchema


class ClockInSchema(BaseModel):
    user_id: UUID


class ClockOutSchema(BaseModel):
    id: UUID

    user: Optional[User]

    user_id: UUID
