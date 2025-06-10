#!/usr/bin/env python3
# File: app/services/pension_service.py
# Author: Oluwatobiloba Light
"""Pension Services"""


from typing import Union
from uuid import UUID
from app.core.exceptions import GeneralError
from app.models.pension import Pension
from app.repositories.pension_repository import PensionRepository
from app.schemas.pension_schema import CreatePensionSchema
from app.services.base_service import BaseService


class PensionService(BaseService):
    def __init__(self, pension_repository: PensionRepository):
        self.pension_repository = pension_repository

        super().__init__(pension_repository)

    async def add_pension(self, pension: CreatePensionSchema) -> Union[Pension, None]:
        """Add a new pension on HRIS"""
        try:
            new_pension = await self.pension_repository.create(pension)
            return new_pension
        except Exception as e:
            raise GeneralError(detail=str(e))

    async def get_by_id(self, id: Union[str, UUID]):
        """Get a pension by id"""
        pension_id: UUID
        try:
            pension_id = UUID(id)
        except (Exception, ValueError) as e:
            raise GeneralError(detail="Pension ID is invalid")

        return await self.pension_repository.get_by_id(pension_id)

    async def get_all(self):
        """ "Get all pensions"""
        try:
            return await self.pension_repository.get_all()
        except Exception as e:
            raise GeneralError(detail=str(e))
