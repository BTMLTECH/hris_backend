#!/usr/bin/env python3
# File: app/models/user_permission.py
# Author: Oluwatobiloba Light
"""User Permission Model"""


from uuid import UUID
from app.models.base_model import BaseModel
from sqlmodel import Field
from sqlalchemy import Column, ForeignKey


class UserPermissionLink(BaseModel, table=True):
    __tablename__: str = "user_permissions"

    user_id: UUID = Field(
        sa_column=Column("user_id", ForeignKey(column="users.id", ondelete="CASCADE"))
    )

    permission_id: UUID = Field(
        sa_column=Column(
            "permission_id", ForeignKey(column="permissions.id", ondelete="CASCADE")
        )
    )
