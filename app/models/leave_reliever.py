#!/usr/bin/env python3
# File: app/models/leave_reliever.py
# Author: Oluwatobiloba Light
"""Leave Reliever Database Model"""


from datetime import date, datetime
from typing import Optional
from uuid import UUID
from sqlalchemy import Boolean, Column, Date, DateTime, Enum, ForeignKey, String
from sqlmodel import Field, Relationship
from app.models.base_model import BaseModel


class LeaveReliever(BaseModel, table=True):
    __tablename__: str = "leave_relievers"

    leave_request_id: UUID = Field(
        sa_column=Column(
            ForeignKey("leave_requests.id", ondelete="CASCADE"),
            nullable=True,
            default=None,
        )
    )

    leave_request: "LeaveRequest" = Relationship(back_populates="leave_relievers")

    reliever_id: UUID = Field(
        sa_column=Column(
            ForeignKey("users.id", ondelete="SET NULL"), nullable=True, default=None
        )
    )

    reliever: Optional["User"] = Relationship()

    approved: bool = Field(sa_column=Column(Boolean, nullable=False, default=False))

    approved_at: Optional[datetime] = Field(
        sa_column=Column(DateTime, nullable=True, default=None)
    )
