#!/usr/bin/env python3
# File: app/api/endpoints/pension.py
# Author: Oluwatobiloba Light
"""Pension endpoint"""

from typing import Sequence
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from app.core.container import Container
from app.core.dependencies import require_roles_and_permissions
from app.models.user import User
from app.schemas.pension_schema import PensionSchema, CreatePensionSchema
from app.services.pension_service import PensionService


router = APIRouter(
    prefix="/pension",
    tags=["Pension"],
)


@router.post(
    "/create",
    response_model=PensionSchema,
    name="Create a Pension record",
    description="This route is used to create a pension record on HRIS",
)
@inject
async def create_pension(
    pension_schema: CreatePensionSchema,
    service: PensionService = Depends(Provide[Container.pension_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin", "hr_admin"],
            required_permissions=["full_access", "limited_access"],
        )
    ),
):
    """Route to create a pension record on HRIS"""
    user = await service.add_pension(pension_schema)

    return user

@router.get("/all", response_model=Sequence,
    name="Get all Pension records",
    description="This route is used to get all pension records on HRIS",)
@inject
async def get_all_pensions(service: PensionService = Depends(Provide[Container.pension_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin", "hr_admin"],
            required_permissions=[],
        )
    ),):
    """Route to get all pension records on HRIS"""
    pensions = await service.get_all()

    return pensions