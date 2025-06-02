#!/usr/bin/env python3
# File: app/schemas/department_schema.py
# Author: Oluwatobiloba Light
"""Department Validation Schema"""

from typing import List, Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID

from app.models.permission import Permission
from app.models.user import User
from app.schemas.base_schema import ModelBaseInfo
from app.schemas.user_schema import UserBaseSchema


# Department
class CreateDepartmentSchema(BaseModel):
    name: str

    description: Optional[str] = None

    team_lead_id: Optional[str] = None


class User_(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    staff_id: int
    job_title: Optional[str]


class ReadDepartmentSchema(ModelBaseInfo):
    name: str
    
    description: Optional[str] = None

    team_lead_id: Optional[UUID] = None

    team_lead: Optional[UserBaseSchema] = None

    team_members: Optional[List[UserBaseSchema]] = None

class UpdateDepartmentSchema(ModelBaseInfo):
    name: Optional[str] = None

    description: Optional[str] = None


class AssignDepartmentTeamLeadSchema(BaseModel):
    team_lead_id: str

    department_id: str

class CreateUserDepartmentSchema(BaseModel):
    user_id: str
    department_id: str
