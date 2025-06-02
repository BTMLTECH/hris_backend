#!/usr/bin/env python3
# File: api/endpoints/attendance.py
# Author: Oluwatobiloba Light
"""Auth endpoint"""

from typing import Sequence
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from app.core.container import Container
from app.core.dependencies import require_roles_and_permissions
from app.models.user import User
from app.schemas.attendance_schema import AttendanceSchema, ClockInSchema
from app.services.attendance_service import AttendanceService


router = APIRouter(
    prefix="/attendance",
    tags=["User Attendance"],
)


@router.post(
    "/clock-in",
    response_model=None,
    name="User attendance clock in on HRIS",
    description="This route is used to clock in as a user on HRIS",
)
@inject
async def user_clock_in(
    service: AttendanceService = Depends(Provide[Container.attendance_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin", "admin", "manager", "team_lead", "employee"],
            required_permissions=[],
        )
    ),
):
    """Route to clock in as a user on HRIS"""
    user = await service.clock_in(current_user)

    return user


@router.post(
    "/clock-out",
    response_model=AttendanceSchema,
    name="User attendance clock out on HRIS",
    description="This route is used to clock out as a user on HRIS",
)
@inject
async def user_clock_out(
    service: AttendanceService = Depends(Provide[Container.attendance_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin", "admin", "manager", "team_lead", "employee"],
            required_permissions=[],
        )
    ),
):
    """Route to clock out as a user on HRIS"""
    user = await service.clock_out(current_user)

    return user


@router.get(
    "/all",
    response_model=Sequence[AttendanceSchema],
    name="User attendance records on HRIS",
    description="This route is used to get all attendance records of a user on HRIS",
)
@inject
async def current_user_attendance(
    service: AttendanceService = Depends(Provide[Container.attendance_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin", "admin", "manager", "team_lead", "employee"],
            required_permissions=[],
        )
    ),
):
    """Route used to get all attendance records of a user on HRIS"""
    attendance_records = await service.get_current_user_attendance_records(
        current_user.id
    )

    return attendance_records
