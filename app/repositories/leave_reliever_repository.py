#!/usr/bin/env python3
# File: repositories/leave_reliever_repository.py
# Author: Oluwatobiloba Light
"""Leave Reliever Repository"""

from datetime import date
from uuid import UUID
from sqlalchemy import select, update
from app.adapter.json_adapter import JSONAdapter
from app.adapter.sqlalchemy_adapter import SQLAlchemyAdapter
from app.models.leave_reliever import LeaveReliever
from typing import List, Optional, Sequence, TypeVar, Union
from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import selectinload
import logging

from app.schemas.leave_schema import CreateLeaveRelieverSchema

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=LeaveReliever)


class LeaveRelieverRepository(BaseRepository):
    def __init__(self, db_adapter: Union[JSONAdapter, SQLAlchemyAdapter]):
        self.db_adapter = db_adapter
        self.model = LeaveReliever

        super().__init__(db_adapter, LeaveReliever)

    async def create(self, leave_reliever_schema=CreateLeaveRelieverSchema):
        """Creates a new leave reliever record in the database"""
        return None
