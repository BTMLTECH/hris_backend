#!/usr/bin/env python3
# File: app/models/role.py
# Author: Oluwatobiloba Light
"""User Roles model"""


from typing import List, Optional
from app.models.base_model import BaseModel
from sqlmodel import Field, Relationship
from sqlalchemy import Column, String

from app.models.role_permission import RolePermissionLink
from app.models.user_role import UserRoleLink


class Role(BaseModel, table=True):
    __tablename__: str = 'roles'

    name: str = Field(sa_column=Column(
        "name", String(255), unique=True, index=True, nullable=False))

    permissions: Optional[List["Permission"] ]= Relationship(
        back_populates="roles",
        link_model=RolePermissionLink,
    )

    users: Optional[List["User"]] = Relationship(back_populates="role", link_model=UserRoleLink)
