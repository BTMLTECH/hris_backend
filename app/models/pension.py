#!/usr/bin/env python3
# File: app/models/pension.py
# Author: Oluwatobiloba Light
"""Pension Database Model"""


from typing import List, Optional
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship
from app.models.base_model import BaseModel
from app.models.user_pension import UserPensionLink


class Pension(BaseModel, table=True):
    __tablename__: str = "pensions"

    name: str = Field(sa_column=Column("name", String(255), nullable=True))

    users: Optional[List["User"]] = Relationship(
        back_populates="pension", link_model=UserPensionLink
    )
