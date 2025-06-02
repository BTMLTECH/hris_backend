#!/usr/bin/env python3
# File: app/schemas/bank_schema.py
# Author: Oluwatobiloba Light
"""Bank Schema"""

from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.user import User
from app.schemas.base_schema import ModelBaseInfo


class CreateBankSchema(BaseModel):
    name: str = Field(..., example="Zenith Bank")


class BankSchema(ModelBaseInfo):
    name: str

    users: Optional[List[User]] = None

    class Config:
        from_attributes = True
