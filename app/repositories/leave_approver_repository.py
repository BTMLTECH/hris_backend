#!/usr/bin/env python3
# File: repositories/leave_approver_repository.py
# Author: Oluwatobiloba Light
"""Leave Approver Repository"""

from datetime import date
from uuid import UUID
from sqlalchemy import select, update
from app.adapter.json_adapter import JSONAdapter
from app.adapter.sqlalchemy_adapter import SQLAlchemyAdapter
from app.models.leave_approver import LeaveApprover
from typing import List, Optional, Sequence, TypeVar, Union
from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import selectinload
import logging

from app.schemas.leave_schema import CreateLeaveApproverSchema

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=LeaveApprover)


class LeaveApproverRepository(BaseRepository):
    def __init__(self, db_adapter: Union[JSONAdapter, SQLAlchemyAdapter]):
        self.db_adapter = db_adapter
        self.model = LeaveApprover

        super().__init__(db_adapter, LeaveApprover)

    async def create(self, leave_approver_schema=CreateLeaveApproverSchema):
        """Creates a new leave approver record in the database"""
        return None
