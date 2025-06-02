#!/usr/bin/env python3
# File: app/schemas/leave_request_schema.py
# Author: Oluwatobiloba Light
"""Leave Request Validation Schema"""

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, model_validator
from uuid import UUID

from app.models.leave_approver import LeaveApprover
from app.models.leave_reliever import LeaveReliever
from app.schemas.base_schema import ModelBaseInfo


# Leave Request
class CreateLeaveRequestSchema(BaseModel):
    user_id: str
    leave_type_id: UUID
    start_date: date
    end_date: date
    reason: Optional[str] = Field(..., min_length=255)
    reliever_ids: List[UUID] = Field(..., min_items=1, max_items=3)
    allowance: bool = False

    @model_validator(mode="after")
    def validate_dates_and_relivers(self):
        start = self.start_date
        end = self.end_date
        relievers = self.reliever_ids

        if start > end:
            raise ValueError("End date must be after start date")

        if not relievers or not (1 <= len(relievers) <= 3):
            raise ValueError("You must select between 1 and 3 relievers")

        return self


class ReadLeaveRequestSchema(ModelBaseInfo):
    id: UUID
    user_id: UUID
    leave_type_id: UUID
    start_date: date
    end_date: date
    reason: Optional[str] = None
    allowance: bool
    status: str
    created_at: date

    relievers: List[LeaveReliever]
    approvers: List[LeaveApprover]

    class Config:
        from_attributes = True


# Leave Reliever
class CreateLeaveRelieverSchema(BaseModel):
    leave_request_id: UUID

    reliever_id: UUID

    approved: bool


class ReadLeaveRelieverSchema(ModelBaseInfo):
    leave_request_id: UUID
    reliever_id: UUID
    approved: bool
    approved_at: Optional[date]

    class Config:
        from_attributes = True


# Leave Approver
class CreateLeaveApproverSchema(BaseModel):
    leave_request_id: UUID
    approver_id: UUID

    role: str
    status: str
    comment: Optional[str] = None


class ReadLeaveApproverSchema(ModelBaseInfo):
    leave_request_id: UUID
    approver_id: UUID

    role: str
    status: str
    comment: Optional[str] = None

    approved_date: date

    class Config:
        from_attributes = True