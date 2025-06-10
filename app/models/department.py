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

    # team_lead_id: Optional[UUID] = Field(
    #     sa_column=Column(
    #         ForeignKey(
    #             "users.id", ondelete="SET NULL", name="fk_departments_team_lead_id"
    #         ),
    #         nullable=True,
    #     )
    # )

    # team_lead_id: Optional[int] = Field(
    #     sa_column=Column(
    #         ForeignKey(
    #             "users.id",
    #             ondelete="SET NULL",
    #             name="fk_departments_team_lead_id",
    #             use_alter=True,
    #         ),
    #         default=None,
    #         nullable=True,
    #     )
    # )

    # team_lead: Optional["User"] = Relationship(
    #     sa_relationship_kwargs={
    #         "foreign_keys": "[User.department_id]",
    #         "overlaps": "department,team_members",
    #     }
    # )

    # team_members: Optional[List["User"]] = Relationship(
    #     back_populates="department",
    #     sa_relationship_kwargs={
    #         "foreign_keys": "[User.department_id]",
    #         "overlaps": "team_lead",
    #     },
    # )

    # team_lead: Optional["User"] = Relationship(
    #     sa_relationship_kwargs={
    #         "foreign_keys": "department_id",
    #         "overlaps": "team_members",
    #     }
    # )

    # team_members: Optional[List["User"]] = Relationship(
    #     back_populates="department",
    #     sa_relationship_kwargs={
    #         "overlaps": "team_lead",
    #     },
    # )
    # Foreign key to User for team lead
    team_lead_id: Optional[UUID] = Field(  # Changed back to UUID to match User.id
        sa_column=Column(
            ForeignKey(
                "users.id",
                ondelete="SET NULL",
                name="fk_departments_team_lead_id",
                use_alter=True,
            ),
            default=None,
            nullable=True,
        )
    )
    
    # Relationship to the team lead user
    team_lead: Optional["User"] = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "[Department.team_lead_id]",  # Use full path and correct FK
            "overlaps": "team_members",
        }
    )
    
    # Relationship to all team members (users who belong to this department)
    team_members: Optional[List["User"]] = Relationship(
        back_populates="department",
        sa_relationship_kwargs={
            "foreign_keys": "[User.department_id]",  # This should reference User's FK to Department
            "overlaps": "team_lead",
        },
    )
