#!/usr/bin/env python3
# File: app/schemas/user_schema.py
# Author: Oluwatobiloba Light
"""User Schema"""


from datetime import date, datetime
from enum import Enum
from typing import List, Literal, Optional, Union
from uuid import UUID
from pydantic import BaseModel, EmailStr

from app.models.attendance import Attendance
from app.models.bank import Bank
from app.models.department import Department
from app.models.employment_type import EmploymentType
from app.models.leave_request import LeaveRequest
from app.models.next_of_kin import NextOfKin
from app.models.payroll import Payroll
from app.models.pension import Pension
from app.models.permission import Permission
from app.models.role import Role
from app.schemas.base_schema import ModelBaseInfo
from app.schemas.role_schema import RoleSchema


class CreateUser(BaseModel):
    # id: UUID = Field( default_factory=uuid4)
    first_name: str
    middle_name: Union[str, None] = None
    last_name: str
    email: EmailStr
    password: str

    staff_id: int
    office_email: EmailStr


class UserSchema(BaseModel):
    first_name: str
    middle_name: Union[str, None] = None
    last_name: str
    email: EmailStr
    password: str

    staff_id: int

    class Config:
        from_attributes = True


class CachedUser(ModelBaseInfo):
    name: str
    email: EmailStr
    # password: Union[str, None] = None
    phone: Union[str, None] = None
    provider: Literal["google", "email"]
    email_verified: bool
    address: Union[str, None] = None

    is_active: bool
    is_admin: bool

    deleted_at: Union[datetime, None] = None
    last_login_at: datetime

    class Config:
        from_attributes = True


class CreateEmploymentTypeSchema(BaseModel):
    name: str

class UpdateEmploymentTypeSchema(BaseModel):
    name: Optional[str] = None

class ReadEmploymentTypeSchema(ModelBaseInfo):
    name: str

    class Config:
        from_attributes = True
        orm_mode = True


#


class UserGenderType(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class UserRoleType(str, Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    HR = "hr"
    DEPARTMENT_LEAD = "department_lead"
    INTERN = "intern"
    SUPER_ADMIN = "super_admin"


class UserBaseSchema(BaseModel):
    id: Optional[UUID] = None
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    gender: Optional[UserGenderType]
    image_uri: Optional[str] = None
    dob: date
    job_title: Optional[str] = None
    staff_id: int
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None

    next_of_kin: Optional[NextOfKin] = None

    attendance: Optional[List[Attendance]] = None
    leave_requests: Optional[List[LeaveRequest]] = None

    department_id: Optional[UUID] = None
    department: Optional[Department] = None

    personal_email: Optional[EmailStr] = None
    employment_date: Optional[datetime] = None

    employment_type_id: Optional[UUID] = None
    employment_type: Optional[EmploymentType] = None

    payroll_class_id: Optional[UUID] = None
    payroll_class: Optional[Payroll] = None
    bank_id: Optional[UUID] = None
    bank: Optional[Bank] = None
    bank_account_number: Optional[str] = None
    tax_number: Optional[str] = None

    pension_id: Optional[UUID] = None
    pension: Optional[Pension] = None
    pension_number: Optional[str] = None

    role_id: Optional[UUID] = None
    role: Optional[RoleSchema] = None

    permissions: Optional[List[Permission]] = None
    is_active: Optional[bool] = True

    class Config:
        # from_attributes = True
        orm_mode = True


class SuperAdminSchema(UserBaseSchema): ...


class UserSchema(UserBaseSchema): ...


class UserUpdateSchema(UserBaseSchema):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[UserGenderType] = None
    image_uri: Optional[str] = None
    dob: Optional[date] = None
    job_title: Optional[str] = None
    staff_id: Optional[int] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None

    next_of_kin: Optional[NextOfKin] = None
    personal_email: Optional[EmailStr] = None
    bank_id: Optional[UUID] = None
    bank: Optional[Bank] = None
    bank_account_number: Optional[str] = None

    department_id: Optional[UUID] = None
    department: Optional[Department] = None

    personal_email: Optional[EmailStr] = None
    employment_date: Optional[datetime] = None

    employment_type_id: Optional[UUID] = None
    employment_type: Optional[EmploymentType] = None

    payroll_class_id: Optional[UUID] = None
    payroll_class: Optional[Payroll] = None
    bank_id: Optional[UUID] = None
    bank: Optional[Bank] = None
    bank_account_number: Optional[str] = None
    tax_number: Optional[str] = None

    pension_id: Optional[UUID] = None
    pension: Optional[Pension] = None
    pension_number: Optional[str] = None

    role_id: Optional[UUID] = None
    role: Optional[RoleSchema] = None

    permissions: Optional[List[Permission]] = None
    is_active: Optional[bool] = True

    class Config:
        from_attributes = True
        orm_mode = True
