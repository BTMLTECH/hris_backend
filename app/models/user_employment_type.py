#!/usr/bin/env python3
# File: app/models/employment_type.py
# Author: Oluwatobiloba Light
"""User Employment Type Model"""

from uuid import UUID
from sqlmodel import Field
from sqlalchemy import Column, ForeignKey
from app.models.base_model import BaseModel


class UserEmploymentTypeLink(BaseModel, table=True):
    __tablename__: str = "user_employment_types"

    user_id: UUID = Field(sa_column=Column(
        "user_id", ForeignKey(column="users.id", ondelete="CASCADE")))

    employment_type_id: UUID = Field(sa_column=Column(
        "employment_type_id", ForeignKey(column="employment_types.id", ondelete="CASCADE")))
