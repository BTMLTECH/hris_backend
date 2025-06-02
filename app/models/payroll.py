#!/usr/bin/env python3
# File: app/models/payroll.py
# Author: Oluwatobiloba Light
"""Payroll Model class"""


from typing import Optional
from sqlalchemy import Column, Numeric, String
from sqlmodel import Field, Relationship
from app.models.base_model import BaseModel


class Payroll(BaseModel, table=True):
    __tablename__: str = "payrolls"

    name: str = Field(sa_column=Column(String, nullable=False, default=None, unique=True))

    basic_pay: float = Field(
        sa_column=Column(Numeric(10, 2), nullable=True, default=None)
    )

    housing_allowance: float = Field(
        sa_column=Column(Numeric(10, 2), nullable=True, default=None)
    )

    transport_allowance: float = Field(
        sa_column=Column(Numeric(10, 2), nullable=True, default=None)
    )
    health_allowance: float = Field(
        sa_column=Column(Numeric(10, 2), nullable=True, default=None)
    )
    total_allowances: float = Field(
        sa_column=Column(Numeric(10, 2), nullable=True, default=None)
    )

    users: Optional["User"] = Relationship(back_populates="payroll_class")
