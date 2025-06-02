#!/usr/bin/env python3
# File: app/models/user_role.py
# Author: Oluwatobiloba Light
"""User Role Model"""

from uuid import UUID
from sqlmodel import Field
from sqlalchemy import Column, ForeignKey
from app.models.base_model import BaseModel


class UserRoleLink(BaseModel, table=True):
    __tablename__: str = "user_roles"

    user_id: UUID = Field(sa_column=Column(
        "user_id", ForeignKey(column="users.id", ondelete="CASCADE")))

    role_id: UUID = Field(sa_column=Column(
        "role_id", ForeignKey(column="roles.id", ondelete="CASCADE")))
