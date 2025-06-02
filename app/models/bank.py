#!/usr/bin/env python3
# File: app/models/bank.py
# Author: Oluwatobiloba Light
"""Bank Database Model"""


from typing import List, Optional
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship
from app.models.base_model import BaseModel
from app.models.user_bank import UserBankLink


class Bank(BaseModel, table=True):
    __tablename__: str = "banks"

    name: str = Field(sa_column=Column("name", String(255), nullable=True))

    users: Optional[List["User"]] = Relationship(
        back_populates="bank"
    )
