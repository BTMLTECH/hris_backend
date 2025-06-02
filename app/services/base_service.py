#!/usr/bin/env python3
# File: app/services/base_service.py
# Author: Oluwatobiloba Light

from typing import Any, TypeVar, Union
from uuid import UUID
from app.core.exceptions import GeneralError
from app.repositories.base_repository import BaseRepository


T = TypeVar("T")


class BaseService:
    def __init__(self, repository: BaseRepository):
        self._repository = repository

    async def add(self, schema: T) -> T:
        """Add a new record."""
        return await self._repository.create(schema)

    async def get_by_id(self, id: Union[str, UUID]) -> Union[Any, None]:
        """Get document by id"""

        try:
            role_id = UUID(role_id)
        except (Exception, ValueError) as e:
            raise GeneralError(detail="Role ID is invalid")
        

        return await self._repository.get_by_id(id)
