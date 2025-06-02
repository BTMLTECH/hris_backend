#!/usr/bin/env python3
# File: app/repositories/base_repository.py
# Author: Oluwatobiloba Light
"""Base Repository"""

from typing import Type, TypeVar
from app.adapter.database_adapter import DatabaseAdapter
from app.adapter.sqlalchemy_adapter import SQLAlchemyAdapter
from app.models.base_model import BaseModel
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator


T = TypeVar('T',  bound=BaseModel)


class BaseRepository:
    def __init__(self, db_adapter: DatabaseAdapter, model: Type[T]) -> None:
        self.db_adapter = db_adapter
        self.model = model

    @asynccontextmanager
    async def session_scope(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.db_adapter.session() as session:
            try:
                async with session.begin():
                    yield session
            except Exception:
                await self.db_adapter.rollback(session)
                raise