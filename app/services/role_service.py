#!/usr/bin/env python3
# File: services/role_service.py
# Author: Oluwatobiloba Light
"""Role Services"""


from typing import Union
from uuid import UUID
from app.core.exceptions import GeneralError
from app.models.role import Role
from app.repositories.role_repository import RoleRepository
from app.schemas.role_schema import CreateRoleSchema
from app.services.base_service import BaseService


class RoleService(BaseService):
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository

        super().__init__(role_repository)

    async def add_role(self, role: CreateRoleSchema) -> Union[Role, None]:
        """Add a new user role on HRIS"""
        try:
            new_role = await self.role_repository.create(role)
            return new_role
        except Exception as e:
            raise GeneralError(detail=str(e))

    async def get_by_id(self, id: Union[str, UUID]):
        """Get a role by id"""
        role_id: UUID
        try:
            role_id = UUID(id)
        except (Exception, ValueError) as e:
            raise GeneralError(detail="Role ID is invalid")

        return await self.role_repository.get_by_id(role_id)

    async def get_all(self):
        """ "Get all roles"""
        try:
            return await self.role_repository.get_all()
        except Exception as e:
            raise GeneralError(detail=str(e))
