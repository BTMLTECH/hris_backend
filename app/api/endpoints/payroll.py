#!/usr/bin/env python3
# File: app/api/endpoints/payroll.py
# Author: Oluwatobiloba Light
"""Payroll endpoint"""

from typing import Sequence
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from app.core.container import Container
from app.core.dependencies import require_roles_and_permissions
from app.models.user import User
from app.schemas.payroll_schema import PayrollSchema, CreatePayrollSchema
from app.services.payroll_service import PayrollService


router = APIRouter(
    prefix="/payroll",
    tags=["Payroll"],
)


@router.post(
    "/create",
    response_model=PayrollSchema,
    name="Create a Payroll record",
    description="This route is used to create a payroll record on HRIS",
)
@inject
async def create_payroll(
    payroll_schema: CreatePayrollSchema,
    service: PayrollService = Depends(Provide[Container.payroll_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin", "hr_admin"],
            required_permissions=["full_access", "limited_access"],
        )
    ),
):
    """Route to create a payroll record on HRIS"""
    user = await service.add_payroll(payroll_schema)

    return user

@router.get("/all", response_model=Sequence[PayrollSchema],
    name="Get all Payroll records",
    description="This route is used to get all payroll records on HRIS",)
@inject
async def get_all_payrolls(service: PayrollService = Depends(Provide[Container.payroll_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin", "hr_admin"],
            required_permissions=[],
        )
    ),):
    """Route to get all payroll records on HRIS"""
    payrolls = await service.get_all()

    return payrolls