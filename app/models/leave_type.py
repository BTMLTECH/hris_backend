#!/usr/bin/env python3
# File: app/models/leave_type.py
# Author: Oluwatobiloba Light
"""Leave Type Database Model"""


from datetime import date
import enum
from typing import Optional
from uuid import UUID
from sqlalchemy import Boolean, Column, Date, Enum, ForeignKey, Integer, String
from sqlmodel import Field
from app.models.base_model import BaseModel


class LeaveType(BaseModel, table=True):
    __tablename__: str = "leave_types"

    name: str = Field(sa_column=Column(String, nullable=False, default=None, unique=True))

    description: Optional[str] = Field(sa_column=Column(String, nullable=True, default=None))

    max_days: int = Field(sa_column=Column(Integer, nullable=False, default=None))
    

    