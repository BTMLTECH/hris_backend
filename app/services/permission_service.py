#!/usr/bin/env python3
# File: services/permission_service.py
# Author: Oluwatobiloba Light
"""Permission Services"""


from typing import Union
from uuid import UUID
from app.core.exceptions import GeneralError
from app.models.permission import Permission
from app.repositories.permission_repository import PermissionRepository
from app.schemas.permission_schema import CreatePermissionSchema
from app.services.base_service import BaseService


class PermissionService(BaseService):
    def __init__(self, permission_repository: PermissionRepository):
        self.permission_repository = permission_repository

        super().__init__(permission_repository)

    async def add_permission(self, permission: CreatePermissionSchema) -> Union[Permission, None]:
        """Add a new user permission on HRIS"""
        try:
            new_permission = await self.permission_repository.create(permission)
            return new_permission
        except Exception as e:
            raise GeneralError(detail=str(e))

    async def get_by_id(self, id: Union[str, UUID]):
        """Get a permission by id"""
        permission_id: UUID
        try:
            permission_id = UUID(id)
        except (Exception, ValueError) as e:
            raise GeneralError(detail="Permission ID is invalid")

        return await self.permission_repository.get_by_id(permission_id)

    async def get_all(self):
        """ "Get all permissions"""
        try:
            return await self.permission_repository.get_all()
        except Exception as e:
            raise GeneralError(detail=str(e))
