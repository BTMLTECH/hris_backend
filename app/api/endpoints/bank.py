#!/usr/bin/env python3
# File: api/endpoints/bank.py
# Author: Oluwatobiloba Light
"""Bank endpoint"""

from typing import Sequence
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from app.core.container import Container
from app.core.dependencies import require_roles_and_permissions
from app.models.user import User
from app.schemas.bank_schema import BankSchema, CreateBankSchema
from app.services.bank_service import BankService


router = APIRouter(
    prefix="/bank",
    tags=["Bank"],
)


@router.post(
    "/create",
    response_model=BankSchema,
    name="Create a Bank record",
    description="This route is used to create a bank record on HRIS",
)
@inject
async def create_bank(
    bank_schema: CreateBankSchema,
    service: BankService = Depends(Provide[Container.bank_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin", "hr_admin"],
            required_permissions=[],
        )
    ),
):
    """Route to create a bank record on HRIS"""
    user = await service.add_bank(bank_schema)

    return user

@router.get("/all", response_model=Sequence[BankSchema],
    name="Get all Bank records",
    description="This route is used to get all bank records on HRIS",)
@inject
async def get_all_banks(service: BankService = Depends(Provide[Container.bank_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin", "hr_admin"],
            required_permissions=[],
        )
    ),):
    """Route to get all bank records on HRIS"""
    banks = await service.get_all()

    return banks