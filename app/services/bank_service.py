#!/usr/bin/env python3
# File: services/bank_service.py
# Author: Oluwatobiloba Light
"""Bank Services"""


from typing import Union
from uuid import UUID
from app.core.exceptions import GeneralError, NotFoundError
from app.models.bank import Bank
from app.repositories.bank_repository import BankRepository
from app.schemas.bank_schema import CreateBankSchema, UpdateBankSchema
from app.services.base_service import BaseService
import logging


logger = logging.getLogger(__name__)


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
        """Get all banks"""
        try:
            return await self.bank_repository.get_all()
        except Exception as e:
            raise GeneralError(detail=str(e))

    async def update_bank_by_id(self, id: str, bank_data: UpdateBankSchema):
        """Update a bank by ID"""
        from uuid import UUID

        try:
            bank_uid = UUID(id)
        except (TypeError, ValueError):
            raise GeneralError(detail="Bank ID is invalid", status_code=400)
        
        try:
            bank_data = await self.get_by_id(id)

            if not bank_data or bank_data is None:
                raise NotFoundError(detail="Bank not found or doesn't exist")
            
            return await self.bank_repository.update_by_id(bank_uid, bank_data)
        except Exception as e:
            logger.error(f"An error has occured while updating bank: {e}")
            raise GeneralError(detail="Could not update Bank")
        
    async def delete_bank_by_id(self, id: str):
        """Delete a bank by ID"""
        from uuid import UUID

        try:
            bank_uid = UUID(id)
        except (TypeError, ValueError):
            raise GeneralError(detail="Bank ID is invalid", status_code=400)
        
        try:
            bank_data = await self.get_by_id(id)

            if not bank_data or bank_data is None:
                raise NotFoundError(detail="Bank not found or doesn't exist")
            
            return await self.bank_repository.delete_by_id(bank_uid)
        except Exception as e:
            logger.error(f"An error has occured while deleting bank: {e}")
            raise GeneralError(detail="Could not delete Bank")