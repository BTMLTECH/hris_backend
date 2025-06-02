#!/usr/bin/env python3
# File: app/models/department.py
# Author: Oluwatobiloba Light
"""Department Database Model"""


from typing import List, Optional
from uuid import UUID
from sqlalchemy import Column, ForeignKey, String
from sqlmodel import Field, Relationship
from app.models.base_model import BaseModel
from app.models.user_department import UserDepartmentLink


class Department(BaseModel, table=True):
    __tablename__: str = "departments"

    name: str = Field(
        sa_column=Column("name", String(255), nullable=False, default=None, unique=True)
    )

    description: Optional[str] = Field(
        sa_column=Column(
            "description",
            String(),
            default=None,
            # nullable=False
        )
    )

    # team_lead_id: Optional[UUID] = Field(
    #     sa_column=Column(
    #         ForeignKey("users.id", ondelete="SET NULL"),
    #         nullable=True,
    #     )
    # )

    # team_lead: Optional["User"] = Relationship()

    # team_members: Optional[List["User"]] = Relationship(back_populates="department", sa_relationship_kwargs={"foreign_keys": "[User.department_id]"})

    team_lead_id: Optional[UUID] = Field(
        sa_column=Column(
            ForeignKey(
                "users.id", ondelete="SET NULL", name="fk_departments_team_lead_id"
            ),
            nullable=True,
        )
    )

    team_lead: Optional["User"] = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "[User.department_id]",
            "overlaps": "department,team_members",
        }
    )

    team_members: Optional[List["User"]] = Relationship(
        back_populates="department",
        sa_relationship_kwargs={
            "foreign_keys": "[User.department_id]",
            "overlaps": "team_lead",
        },
    )
