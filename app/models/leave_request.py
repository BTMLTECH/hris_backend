#!/usr/bin/env python3
# File: app/models/leave.py
# Author: Oluwatobiloba Light
"""Leave Database Model"""


from datetime import date
import enum
from typing import List, Optional
from uuid import UUID
from sqlalchemy import Boolean, Column, Date, Enum, ForeignKey, String
from sqlmodel import Field, Relationship
from app.models.base_model import BaseModel


class LeaveRequestType(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"

class LeaveRequest(BaseModel, table=True):
    __tablename__: str = "leave_requests"

    user_id: UUID = Field(
        sa_column=Column(
            "user_id",
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=True,
        )
    )

    user: "User" = Relationship(back_populates="leave_requests")

    leave_type_id: UUID = Field(
        sa_column=Column(
            "leave_type",
            ForeignKey("leave_types.id", ondelete="SET NULL"),
            nullable=True,
        )
    )

    reason: Optional[str] = Field(sa_column=Column("reason", String, nullable=True, default=None))

    start_date: date = Field(nullable=False, default=None)

    end_date: date = Field(sa_column=Column(Date, nullable=False, default=None))

    allowance: bool = Field(sa_column=Column(Boolean, nullable=True, default=False))

    status: LeaveRequestType = Field(sa_column=Column(
            Enum(LeaveRequestType, name="leave_request_type_enum"),
            default=LeaveRequestType.PENDING,
            nullable=True,
        ))
    
    leave_approvers: List["LeaveApprover"] = Relationship(back_populates="leave_request")
    leave_relievers: List["LeaveReliever"] = Relationship(back_populates="leave_request")
