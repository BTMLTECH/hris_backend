#!/usr/bin/env python3
# File: app/models/next_of_kin.py
# Author: Oluwatobiloba Light
"""Next Of Kin Database Model"""


from typing import Optional
from uuid import UUID
from sqlalchemy import Column, ForeignKey, String
from sqlmodel import Field, Relationship
from app.models.base_model import BaseModel
from app.models.user import User


class NextOfKin(BaseModel, table=True):
    __tablename__: str = "next_of_kins"

    name: str = Field(sa_column=Column("name", String(255), nullable=True))

    phone: str = Field(sa_column=Column("phone", String(255), nullable=True))

    email: str = Field(sa_column=Column("email", String(255), nullable=True))

    relationship: str = Field(
        sa_column=Column("relationship", String(255), nullable=True)
    )

    user_id: Optional[UUID] = Field(
        sa_column=Column(
            "user_id", ForeignKey(column="users.id", ondelete="CASCADE"), default=None
        )
    )

    user: Optional[User] = Relationship(back_populates="next_of_kin")

