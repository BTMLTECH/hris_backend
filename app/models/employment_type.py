#!/usr/bin/env python3
# File: app/models/employment_type.py
# Author: Oluwatobiloba Light
"""Employment Type Database Model"""


from typing import List, Optional
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship
from app.models.base_model import BaseModel
from app.models.user_employment_type import UserEmploymentTypeLink


class EmploymentType(BaseModel, table=True):
    __tablename__: str = "employment_types"

    name: str = Field(sa_column=Column(String, default=None, nullable=False, unique=True))
    # users: Optional[List["User"]] = Relationship(back_populates="employment_type", link_model=UserEmploymentTypeLink)
