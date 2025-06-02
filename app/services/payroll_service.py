#!/usr/bin/env python3
# File: app/services/payroll_service.py
# Author: Oluwatobiloba Light
"""Payroll Services"""


from typing import Union
from uuid import UUID
from app.core.exceptions import GeneralError
from app.models.payroll import Payroll
from app.repositories.payroll_repository import PayrollRepository
from app.schemas.payroll_schema import CreatePayrollSchema
from app.services.base_service import BaseService


class PayrollService(BaseService):
    def __init__(self, payroll_repository: PayrollRepository):
        self.payroll_repository = payroll_repository

        super().__init__(payroll_repository)

    async def add_payroll(self, payroll: CreatePayrollSchema) -> Union[Payroll, None]:
        """Add a new payroll on HRIS"""
        try:
            new_payroll = await self.payroll_repository.create(payroll)
            return new_payroll
        except Exception as e:
            raise GeneralError(detail=str(e))

    async def get_by_id(self, id: Union[str, UUID]):
        """Get a payroll by id"""
        payroll_id: UUID
        try:
            payroll_id = UUID(id)
        except (Exception, ValueError) as e:
            raise GeneralError(detail="Payroll ID is invalid")

        return await self.payroll_repository.get_by_id(payroll_id)

    async def get_all(self):
        """ "Get all payrolls"""
        try:
            return await self.payroll_repository.get_all()
        except Exception as e:
            raise GeneralError(detail=str(e))
