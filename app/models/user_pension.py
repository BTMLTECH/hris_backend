#!/usr/bin/env python3
# File: app/models/user_pension.py
# Author: Oluwatobiloba Light
"""User Pension Model"""

from uuid import UUID
from sqlmodel import Field
from sqlalchemy import Column, ForeignKey
from app.models.base_model import BaseModel


class UserPensionLink(BaseModel, table=True):
    __tablename__: str = "user_pensions"

    user_id: UUID = Field(sa_column=Column(
        "user_id", ForeignKey(column="users.id", ondelete="CASCADE")))

    pension_id: UUID = Field(sa_column=Column(
        "pension_id", ForeignKey(column="pensions.id", ondelete="CASCADE")))
