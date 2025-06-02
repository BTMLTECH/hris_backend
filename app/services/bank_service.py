#!/usr/bin/env python3
# File: services/bank_service.py
# Author: Oluwatobiloba Light
"""Bank Services"""


from typing import Union
from uuid import UUID
from app.core.exceptions import GeneralError
from app.models.bank import Bank
from app.repositories.bank_repository import BankRepository
from app.schemas.bank_schema import CreateBankSchema
from app.services.base_service import BaseService


class BankService(BaseService):
    def __init__(self, bank_repository: BankRepository):
        self.bank_repository = bank_repository

        super().__init__(bank_repository)

    async def add_bank(self, bank: CreateBankSchema) -> Union[Bank, None]:
        """Add a new bank on HRIS"""
        try:
            new_bank = await self.bank_repository.create(bank)
            return new_bank
        except Exception as e:
            raise GeneralError(detail=str(e))

    async def get_by_id(self, id: Union[str, UUID]):
        """Get a bank by id"""
        bank_id: UUID
        try:
            bank_id = UUID(id)
        except (Exception, ValueError) as e:
            raise GeneralError(detail="Bank ID is invalid")

        return await self.bank_repository.get_by_id(bank_id)

    async def get_all(self):
        """ "Get all banks"""
        try:
            return await self.bank_repository.get_all()
        except Exception as e:
            raise GeneralError(detail=str(e))
