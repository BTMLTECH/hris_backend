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
from app.schemas.bank_schema import CreateBankSchema, ReadBankSchema, UpdateBankSchema
from app.services.bank_service import BankService


router = APIRouter(
    prefix="/bank",
    tags=["Bank"],
)


@router.post(
    "/create",
    response_model=ReadBankSchema,
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


@router.get(
    "/all",
    response_model=Sequence[ReadBankSchema],
    name="Get all Bank records",
    description="This route is used to get all bank records on HRIS",
)
@inject
async def get_all_banks(
    service: BankService = Depends(Provide[Container.bank_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin", "hr_admin"],
            required_permissions=[],
        )
    ),
):
    """Route to get all bank records on HRIS"""
    banks = await service.get_all()

    return banks


@router.patch(
    "/{bank_id}/update",
    response_model=ReadBankSchema,
    name="Update bank record",
    description="This route is used  to update a bank record on HRIS",
)
@inject
async def update_bank(
    bank_id: str,
    bank: UpdateBankSchema,
    service: BankService = Depends(Provide[Container.bank_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin", "hr_admin"],
            required_permissions=[],
        )
    ),
):
    """Route to update a Bank by ID"""
    return await service.update_bank_by_id(bank_id, bank)


@router.delete(
    "/{bank_id}/delete",
    response_model=ReadBankSchema,
    name="Delete bank record",
    description="This route is used to delete a bank record on HRIS",
)
@inject
async def delete_bank(
    bank_id: str,
    service: BankService = Depends(Provide[Container.bank_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin", "hr_admin"],
            required_permissions=[],
        )
    ),
):
    """Route to update a Bank by ID"""
    bank = await service.delete_bank_by_id(bank_id)

    return bank
