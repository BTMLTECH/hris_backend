#!/usr/bin/env python3
# File: user_schema.py
# Author: Oluwatobiloba Light
"""User Schema"""

from datetime import date, datetime
import re
from typing import List, Optional, Union
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.models.role import Role
from app.models.user import UserGenderType
from app.schemas.base_schema import ModelBaseInfo
from app.schemas.user_schema import SuperAdminSchema, UserBaseSchema, UserSchema


class SignIn(BaseModel):
    email: str
    password: Optional[str] = Field(default=None)


class UserSignUpSchema(UserBaseSchema):
    password: str = Field(..., min_length=6)
    staff_id: Optional[int] = None
    user_role: Optional[str] = None
    user_permissions: Optional[List[str]] = None
    ...

    class Config:
        from_attributes = True


class UserSignUpResponseSchema(BaseModel):
    message: str
    data: Optional[SuperAdminSchema] = None

    class Config:
        from_attributes = True


class CreateUserSchema(BaseModel):
    # Names
    first_name: str = Field(
        min_length="2", example="John", description="User first name"
    )
    middle_name: Union[str, None] = Field(min_length="0", default=None, example="F")
    last_name: str = Field(min_length="2", example="Doe")

    # Contact
    email: EmailStr = Field(..., example="johndoe@example.com")
    password: str = Field(..., example="securePassword1")

    # Gender
    gender: Union[UserGenderType, None] = Field(default=UserGenderType.MALE)

    # DOB
    dob: date

    # Office Information
    job_title: Union[str, None] = Field(default=None)

    # staff_id: int = Field(...)

    class Config:
        error_msg_templates = {
            "value_error.email": "Email address is not valid!",
        }


class LoginSchema(BaseModel):
    email: str = Field(
        ...,  # ... means required
        description="User's email address",
        error_messages={
            "required": "Email is required to log in",
            "type_error": "Email must be a valid string",
            "value_error": "Please provide a valid email address",
        },
    )

    password: Optional[str]

    @field_validator("email")
    def validate_email(cls, v):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        if not re.match(email_regex, v):
            raise ValueError("Invalid email address")
        if not v:
            raise ValueError("Email cannot be empty")
        if not "@" in v:
            raise ValueError("Invalid email format")
        return v

    # @field_validator('password')
    # def password_must_be_strong(cls, v):
    #     if len(v) < 8:
    #         raise ValueError("Password must be at least 8 characters long")
    #     if not any(c.isupper() for c in v):
    #         raise ValueError(
    #             "Password must contain at least one uppercase letter")
    #     return v

    class Config:
        from_attributes = True


class Payload(BaseModel):
    id: str
    email: str
    name: str
    roles: Optional[List[Role]] = None


class SignInResponse(BaseModel):
    access_token: str
    csrf_token: str
    user: UserSchema


class SignUpResponse(BaseModel):
    new_user: UserSchema


class VerifyUser(BaseModel):
    session_id: str


class ForgotPasswordSchema(BaseModel):
    email: EmailStr
