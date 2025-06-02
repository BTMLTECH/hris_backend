#!/usr/bin/env python3
# File: app/models/user.py
# Author: Oluwatobiloba Light
"""User Model"""


from datetime import date, datetime, timedelta
import enum
from typing import List, Optional, Union
from uuid import uuid4, UUID
from pydantic import EmailStr
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Sequence,
    String,
    Boolean,
    Enum,
    Integer,
    ForeignKey,
)
from sqlalchemy.sql import func
from sqlmodel import Field, Relationship
from app.models.base_model import BaseModel
from app.models.user_bank import UserBankLink
from app.models.user_department import UserDepartmentLink
from app.models.user_employment_type import UserEmploymentTypeLink
from app.models.user_pension import UserPensionLink
from app.models.user_permission import UserPermissionLink
from app.models.user_role import UserRoleLink


class UserGenderType(str, enum.Enum):
    """User Gender Type"""

    MALE = "MALE"
    FEMALE = "FEMALE"


# UserGenderTypeEnum: Enum = Enum(
#     UserGenderType,
#     name="user_gender_type_enum",
#     create_constraint=True,
#     metadata=BaseModel.metadata,
#     validate_strings=True,
# )

field_sequence = Sequence("staff_id_seq", start=1, increment=1)


class User(BaseModel, table=True):
    __tablename__: str = "users"

    # Basic Personal Information
    first_name: str = Field(sa_column=Column("first_name", String(255), nullable=False))

    middle_name: str = Field(
        sa_column=Column("middle_name", String(255), nullable=True)
    )

    last_name: str = Field(sa_column=Column("last_name", String(255), nullable=False))

    gender: Union[UserGenderType, None] = Field(
        sa_column=Column(
            "gender",
            Enum(UserGenderType, name="user_gender_type_enum",  create_type=False),
            default=None,
            nullable=True,
        )
    )

    image_uri: str = Field(sa_column=Column("image_uri", String(255), nullable=True))

    dob: date = Field(
        default_factory=lambda: date.today(),
        nullable=False,
        sa_column_kwargs={"server_default": func.current_date()},
    )

    job_title: Union[str, None] = Field(
        sa_column=Column("job_title", String(255), nullable=True, default=None)
    )

    staff_id: int = Field(
        sa_column=Column(
            Integer,
            nullable=False,
            default=func.nextval("staff_id_seq"),
            autoincrement=True,
        )
    )

    # Authentication
    password: str = Field(
        sa_column=Column(
            "password",
            String(255),
            default="Balila@123###",
            nullable=False,
        )
    )

    # Contact
    email: EmailStr = Field(
        sa_column=Column("email", String(255), unique=True, nullable=False)
    )

    phone: Union[str, None] = Field(
        sa_column=Column(
            "phone",
            String(24),
            default=None,
            nullable=True,
        )
    )

    address: Union[str, None] = Field(
        sa_column=Column(
            "address",
            String(255),
            default=None,
            nullable=True,
        )
    )

    city: Union[str, None] = Field(
        sa_column=Column(
            "city",
            String(255),
            default=None,
            nullable=True,
        )
    )

    state: Union[str, None] = Field(
        sa_column=Column("state", String(255), default=None, nullable=True)
    )

    country: Union[str, None] = Field(
        sa_column=Column("country", String(255), default=None, nullable=True)
    )

    # Relationship to Next of kin
    next_of_kin: Optional["NextOfKin"] = Relationship(back_populates="user")

    # Office information
    personal_email: EmailStr = Field(
        sa_column=Column("personal_email", String(255), unique=True, nullable=True)
    )

    # Attendance Records
    attendance: Optional[List["Attendance"]] = Relationship(back_populates="user")

    # Leave requests
    leave_requests: Optional[List["LeaveRequest"]] = Relationship(back_populates="user")

    department_id: Optional[UUID] = Field(
        sa_column=Column(
            ForeignKey(column="departments.id", name="fk_users_department_id"), nullable=True, default=None
        )
    )
    department: Optional["Department"] = Relationship(
        back_populates="team_members", sa_relationship_kwargs={"foreign_keys": "[User.department_id]"}
    )


    employment_date: date = Field(
        sa_column=Column("employment_date", Date, server_default=func.now()),
        default_factory=date.today,
    )

    employment_type_id: Optional[UUID] = Field(
        sa_column=Column(
            ForeignKey(column="employment_types.id"), nullable=True, default=None
        )
    )

    employment_type: Optional["EmploymentType"] = Relationship(
        # back_populates="users"
    )

    # Account information
    payroll_class_id: Optional[UUID] = Field(
        sa_column=Column(ForeignKey(column="payrolls.id"), nullable=True, default=None)
    )

    payroll_class: Optional["Payroll"] = Relationship(back_populates="users")

    tax_number: str = Field(sa_column=Column("tax_number", String(255), nullable=True))

    # Relationship to Bank
    bank_id: Optional[UUID] = Field(
        sa_column=Column("bank_id", ForeignKey(column="banks.id"), default=None, nullable=True)
    )

    bank: Optional["Bank"] = Relationship(
        back_populates="users"
    )

    bank_account_number: str = Field(
        sa_column=Column("bank_account_number", String(255), nullable=True)
    )

    # Relationship to Pension
    pension_id: Optional[UUID] = Field(
        sa_column=Column("pension_id", ForeignKey(column="pensions.id"), default=None)
    )

    pension: Optional["Pension"] = Relationship(
        back_populates="users", link_model=UserPensionLink
    )

    pension_number: str = Field(
        sa_column=Column("pension_number", String(255), nullable=True)
    )

    role_id: UUID =  Field(
        sa_column=Column("role_id", ForeignKey(column="roles.id"), default=None)
    )

    role: Optional["Role"] = Relationship(
        back_populates="users", link_model=UserRoleLink
    )

    permissions: Optional[List["Permission"]] = Relationship(
        back_populates="users", link_model=UserPermissionLink
    )

    is_active: bool = Field(
        sa_column=Column("is_active", Boolean, default=True, nullable=True)
    )

    last_login_at: datetime = Field(
        sa_column=Column(
            "last_login_at", DateTime(timezone=True), server_default=func.now()
        ),
        default_factory=datetime.now,
    )
