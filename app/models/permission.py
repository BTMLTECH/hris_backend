#!/usr/bin/env python3
# File: app/models/permission.py
# Auhtor: Oluwatobiloba Light
"""Permission Model"""


from typing import List, Optional
from app.models.base_model import BaseModel
from uuid import UUID
from sqlmodel import Field, Relationship
from sqlalchemy import ForeignKey, Column, String

from app.models.role_permission import RolePermissionLink
from app.models.user_permission import UserPermissionLink


class Permission(BaseModel, table=True):
    __tablename__: str = "permissions"

    name: str = Field(sa_column=Column("name", String(255),unique=True, index=True, nullable=False))

    roles: Optional[List["Role"]] = Relationship(
        back_populates="permissions",
        link_model=RolePermissionLink
    )

    users: Optional[List["User"]] = Relationship(back_populates="permissions", link_model=UserPermissionLink)
