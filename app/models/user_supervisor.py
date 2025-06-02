#!/usr/bin/env python3
# File: app/models/supervisor.py
# Author: Oluwatobiloba Light
"""User Supervisor model"""


from typing import List, Optional
from uuid import UUID
from app.models.base_model import BaseModel
from sqlmodel import Field, Relationship
from sqlalchemy import Column, ForeignKey, String


class UserSupervisor(BaseModel, table=True):
    __tablename__: str = 'user_supervisors'

    role: str = Field(sa_column=Column(String(50), unique=True, index=True, nullable=False))

    user_id: UUID = Field(
        sa_column=Column(
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=True,
        )
    )

    supervisor_id: UUID = Field(
        sa_column=Column(
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=True,
        )
    )