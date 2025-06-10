#!/usr/bin/env python3
# File: app/schemas/payroll_schema.py
# Author: Oluwatobiloba Light
"""Payroll Schema"""

from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.user import User
from app.schemas.base_schema import ModelBaseInfo
from app.schemas.user_schema import UserBaseSchema


class CreatePayrollSchema(BaseModel):
    name: str
    basic_pay: float

    housing_allowance: Optional[float] = None

    transport_allowance: Optional[float] = None
    health_allowance: Optional[float] = None
    total_allowances: Optional[float] = None


class PayrollSchema(ModelBaseInfo):
    name: str
    basic_pay: float

    housing_allowance: Optional[float] = None

    transport_allowance: Optional[float] = None
    health_allowance: Optional[float] = None
    total_allowances: Optional[float] = None

    users: Optional[List[UserBaseSchema]] = None

    class Config:
        orm_mode = True
