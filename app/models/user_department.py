#!/usr/bin/env python3
# File: app/models/user_department.py
# Author: Oluwatobiloba Light
"""User Department Model"""

from uuid import UUID
from sqlmodel import Field
from sqlalchemy import Column, ForeignKey
from app.models.base_model import BaseModel


class UserDepartmentLink(BaseModel, table=True):
    __tablename__: str = "user_departments"

    user_id: UUID = Field(sa_column=Column(
        "user_id", ForeignKey(column="users.id", ondelete="CASCADE")))

    department_id: UUID = Field(sa_column=Column(
        "department_id", ForeignKey(column="departments.id", ondelete="CASCADE")))
