#!/usr/bin/env python3
# File: schemas/role_schema.py
# Author: Oluwatobiloba Light
"""Role Schema"""

from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.permission import Permission
from app.models.role import Role
from app.schemas.base_schema import ModelBaseInfo


class CreateRoleSchema(BaseModel):
    name: str = Field(..., example="admin")
    permissions: Optional[List["CreatePermissionSchema"]] = []


class RoleSchema(ModelBaseInfo):
    name: str

    permissions: Optional[List[Permission]] = None

    class Config:
        from_attributes = True
