#!/usr/bin/env python3
# File: app/models/attendance.py
# Author: Oluwatobiloba Light
"""Attendance Database Model"""


from datetime import datetime, date, time
from typing import Optional
from uuid import UUID
from sqlalchemy import Column, Enum, ForeignKey, Numeric
from sqlmodel import Field, Relationship
from app.models.base_model import BaseModel
from sqlalchemy.sql import func
import enum


class AttendanceStatusType(str, enum.Enum):
    """User Attendance Type"""

    ACCURATE = "ACCURATE"
    EARLY = "EARLY"
    LATE = "LATE"


AttendanceStatusTypeEnum: Enum = Enum(
    AttendanceStatusType,
    name="attendance_type_enum",
    create_constraint=True,
    metadata=BaseModel.metadata,
    validate_strings=True,
)


class AttendanceClockStatusType(str, enum.Enum):
    """User Attendance Type"""

    EARLY = "EARLY"
    LATE = "LATE"
    PRESENT = "PRESENT"


AttendanceClockStatusTypeEnum: Enum = Enum(
    AttendanceClockStatusType,
    name="attendance_clock_type_enum",
    create_constraint=True,
    metadata=BaseModel.metadata,
    validate_strings=True,
)


class Attendance(BaseModel, table=True):
    __tablename__: str = "attendance"

    status: Optional[AttendanceStatusType] = Field(
        sa_column=Column(
            "status",
            Enum(AttendanceStatusType, name="attendance_type_enum"),
            default=None,
            nullable=True,
        )
    )

    total_hours: Optional[float] = Field(
        sa_column=Column(Numeric(10, 2), nullable=True)
    )

    clock_in_status: Optional[AttendanceClockStatusType] = Field(
        sa_column=Column(
            "clock_in_status",
            Enum(AttendanceClockStatusType, name="attendance_clock_type_enum"),
            # default=None,
            nullable=False,
        )
    )

    clock_out_status: Optional[AttendanceClockStatusType] = Field(
        sa_column=Column(
            "clock_out_status",
            Enum(AttendanceClockStatusType, name="attendance_clock_type_enum"),
            default=None,
            nullable=True,
        )
    )

    clock_in_date: date = Field(
        default_factory=lambda: date.today(),
        nullable=False,
        sa_column_kwargs={"server_default": func.current_date()},
    )

    clock_in_time: Optional[time] = Field(
        default_factory=lambda: datetime.now().time(),
        nullable=False,
        sa_column_kwargs={"server_default": func.current_time()},
    )

    clock_out_time: Optional[time] = Field(
        # default_factory=lambda: time(12, 00),
        default=None,
        nullable=True,
        # sa_column_kwargs={"server_default": time(12, 00)},
    )

    user_id: UUID = Field(
        sa_column=Column(
            "user_id",
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        )
    )

    user: "User" = Relationship(back_populates="attendance")
