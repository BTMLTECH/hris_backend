#!/usr/bin/env python3
# File: app/models/role_permission.py
# Author: Oluwatobiloba Light
"""Role-Permission Link Model"""


from uuid import UUID
from app.models.base_model import BaseModel
from sqlmodel import Field
from sqlalchemy import Column, ForeignKey


class RolePermissionLink(BaseModel, table=True):
    __tablename__: str = 'role_permissions'

    role_id: UUID = Field(sa_column=Column(
        "role_id", ForeignKey(column="roles.id", ondelete="CASCADE")))

    permission_id: UUID = Field(sa_column=Column(
        "permission_id", ForeignKey(column="permissions.id", ondelete="CASCADE")))
