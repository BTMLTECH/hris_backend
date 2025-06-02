#!/usr/bin/env python3
# File: schemas/permission_schema.py
# Author: Oluwatobiloba Light
"""Role Schema"""

from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.role import Role
from app.schemas.base_schema import ModelBaseInfo
from app.schemas.role_schema import CreateRoleSchema


class CreatePermissionSchema(BaseModel):
    name: str = Field(..., example="admin")
    roles: Optional[List[CreateRoleSchema]] = []


class PermissionSchema(ModelBaseInfo):
    name: str

    roles: Optional[List[Role]] = None

    class Config:
        from_attributes = True
