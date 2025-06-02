#!/usr/bin/env python3
# File: app/models/user_bank.py
# Author: Oluwatobiloba Light
"""User Bank Model"""

from uuid import UUID
from sqlmodel import Field
from sqlalchemy import Column, ForeignKey
from app.models.base_model import BaseModel


class UserBankLink(BaseModel, table=True):
    __tablename__: str = "user_banks"

    user_id: UUID = Field(sa_column=Column(
        "user_id", ForeignKey(column="users.id", ondelete="CASCADE")))

    bank_id: UUID = Field(sa_column=Column(
        "bank_id", ForeignKey(column="banks.id", ondelete="CASCADE")))
