#!/usr/bin/env python3
# File: app/models/leave_approver.py
# Author: Oluwatobiloba Light
"""Leave Approver Database Model"""


from datetime import date
from typing import Optional
from uuid import UUID
from sqlalchemy import Boolean, Column, Date, Enum, ForeignKey, String
from sqlmodel import Field, Relationship
from app.models.base_model import BaseModel


class LeaveApprover(BaseModel, table=True):
    __tablename__: str = "leave_approvers"

    approver_id: UUID = Field(
        sa_column=Column(
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=True,
            default=None
        )
    )
    

    leave_request_id: UUID = Field(sa_column=Column(ForeignKey("leave_requests.id", ondelete="CASCADE"),
            nullable=True, default=None))
    
    
    approver: Optional["User"] = Relationship()
    
    leave_request: "LeaveRequest" = Relationship(back_populates="leave_approvers")
    
    role: str = Field(sa_column=Column(String, nullable=False, default=None))

    status: str = Field(sa_column=Column(String, nullable=False, default=None))

    comment: Optional[str] = Field(sa_column=Column(String, nullable=True, default=None))

    approved_date: date = Field(nullable=False, default=None)
