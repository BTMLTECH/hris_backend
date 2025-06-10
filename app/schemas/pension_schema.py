#!/usr/bin/env python3
# File: app/schemas/pension_schema.py
# Author: Oluwatobiloba Light
"""Pension Schema"""

from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.user import User
from app.schemas.base_schema import ModelBaseInfo
from app.schemas.user_schema import UserBaseSchema


class CreatePensionSchema(BaseModel):
    name: str


class PensionSchema(ModelBaseInfo):
    name: str
    users: Optional[List[UserBaseSchema]] = None

    class Config:
        orm_mode = True
