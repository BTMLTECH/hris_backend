#!/usr/bin/env python3
# File: app/models/base_model.py
# Author: Oluwatobiloba Light
"""Database Base Model"""


from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from sqlalchemy.sql import func
from app.core.database import Base


class BaseModel(Base, SQLModel):
    __abstract__ = True

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False
    )

    created_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_column_kwargs={
            'server_default': func.now()
        }
    )

    updated_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_column_kwargs={
            'server_default': func.now(),
            'onupdate': func.now()
        }
    )
