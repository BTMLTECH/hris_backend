#!/usr/bin/env python3
# File: api/endpoints/user.py
# Author: Oluwatobiloba Light
"""Admin endpoint"""

from typing import Optional, Sequence
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from app.core.container import Container
from app.core.dependencies import require_roles_and_permissions
from app.models.user import User
from app.schemas.auth_schema import UserSignUpResponseSchema, UserSignUpSchema
from app.schemas.user_schema import (
    CreateEmploymentTypeSchema,
    ReadEmploymentTypeSchema,
    UpdateEmploymentTypeSchema,
    UserSchema,
    UserUpdateSchema,
)
from app.services.user_service import UserService


router = APIRouter(
    prefix="/admin",
    tags=["Users: Super Admin, Admin, HR, Department Lead"],
)


# User management
@router.post(
    "/create",
    response_model=UserSignUpResponseSchema,
    name="Create a new super admin user",
    description="This route is used to create a super admin on HRIS",
)
@inject
async def create_super_user_account(
    super_admin_info: UserSignUpSchema,
    service: UserService = Depends(Provide[Container.user_service]),
    # current_user: User = Depends(
    #     require_roles_and_permissions(
    #         required_roles=[""], required_permissions=[""]
    #     )
    # ),
):
    """Route to sign up as a super admin on HRIS"""
    user = await service.create_user(super_admin_info)

    return {"message": "Super admin created successffully", "data": user}


@router.post(
    "/create/employee",
    response_model=UserSignUpResponseSchema,
    name="Create a new user",
    description="This route is used to create a new user on HRIS",
)
@inject
async def create_employee_account(
    employee_info: UserSignUpSchema,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin", "hr", "manager"],
            required_permissions=[],
        )
    ),
):
    """Route to create an employee account on HRIS"""
    user = await service.create_user(employee_info)

    return {"message": "Employee created successffully", "data": user}


@router.get(
    "/employee/{user_id}/view",
    response_model=UserSchema,
    name="Get a user by id",
    description="This route is used to get a user by their ID on HRIS",
)
@inject
async def get_user_by_id(
    user_id: str,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=[
                "super_admin",
                "hr",
                "manager",
            ],
            required_permissions=[],
        )
    ),
):
    """Route to get an employee account by ID on HRIS"""
    user = await service.get_by_id(user_id)

    return user


@router.get(
    "/users/all",
    response_model=Sequence[UserSchema],
    name="Get all users on HRIS",
    description="This route is used to get all users on HRIS",
)
@inject
async def get_all_users(
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin", "hr"], required_permissions=[]
        )
    ),
):
    """Route to get all users on HRIS"""
    user = await service.get_all()

    return user


@router.delete(
    "/employee/{user_id}/delete",
    # response_model=UserSchema,
    name="Delete a user by id",
    description="This route is used to delete a user by their ID on HRIS",
)
@inject
async def delete_user_by_id(
    user_id: str,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=[
                "super_admin",
                "hr",
            ],
            required_permissions=[],
        )
    ),
):
    """Route to delete an employee account by ID on HRIS"""
    user = await service.delete_by_id(user_id)

    return user

@router.post(
    "/employee/{user_id}/activate",
    name="Activate a user using their ID",
    description="This route is used to re-activate a user by their ID on HRIS",
)
@inject
async def activate_user(
    user_id: str,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=[
                "super_admin",
                "hr",
            ],
            required_permissions=[],
        )
    ),
):
    """Route to Activate an employee on HRIS"""
    user = await service.activate_employee(user_id)

    return user


@router.post(
    "/employee/{user_id}/deactivate",
    name="Deactivate a user using their ID",
    description="This route is used to deactivate a user by their ID on HRIS",
)
@inject
async def deactivate_user(
    user_id: str,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=[
                "super_admin",
                "hr",
            ],
            required_permissions=[],
        )
    ),
):
    """Route to Deactivate an employee on HRIS"""
    user = await service.deactivate_employee(user_id)

    return user


@router.get(
    "/profile",
    response_model=UserSchema,
    name="A user profile on HRIS",
    description="This route is used to get a user profile on HRIS",
)
@inject
async def get_user_profile(
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=[
                "super_admin",
                "hr",
                "manager",
                "department_lead",
                "employee",
            ],
            required_permissions=[],
        )
    ),
):
    """Route to get a user profile on HRIS"""
    return current_user

@router.patch(
    "/employee/{user_id}/edit",
    response_model=UserSchema,
    name="Edit an employee's profile",
    description="This route allows an admin to edit an employee's profile on HRIS",
)
@inject
async def edit_employee_profile(
    user_id: str,
    updated_user_info: UserUpdateSchema,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin", "hr", "manager", "department_lead"],
            required_permissions=[],
        )
    ),
):
    """Route to edit an employee's profile on HRIS"""
    user = await service.edit_employee_profile(user_id, updated_user_info)
    return user

@router.post(
    "/profile/edit",
    response_model=None,
    name="Edit a currently logged in user profile on HRIS",
    description="This route is used to edit a user profile on HRIS",
)
@inject
async def edit_user_profile(
    updated_user_info: UserUpdateSchema,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin", "hr", "manager", "department_lead"],
            required_permissions=[],
        )
    ),
):
    """Route to edit a user profile on HRIS"""
    user = await service.update_user_profile(current_user, updated_user_info)
    return user


# EMPLOYMENT TYPES
@router.post(
    "/employment-type/create",
    response_model=ReadEmploymentTypeSchema,
    name="Create an employment type",
    description="This route is used to create an employment type on HRIS",
)
@inject
async def create_employment_type(
    employment_type_info: CreateEmploymentTypeSchema,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin", "manager", "hr"],
            required_permissions=["full_access"],
        )
    ),
):
    """Route to create an employee account on HRIS"""
    employment_type = await service.add_emplyoment_type(employment_type_info)

    return employment_type


@router.get(
    "/employment-type/all",
    response_model=Sequence[ReadEmploymentTypeSchema],
    name="Create an employment type",
    description="This route is used to create an employment type on HRIS",
)
@inject
async def get_all_employment_types(
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin", "manager", "hr"],
            required_permissions=[],
        )
    ),
):
    """Route to create an employee account on HRIS"""
    employment_types = await service.get_employment_types()

    return employment_types


@router.patch(
    "/employment-type/{employment_type_id}/update",
    response_model=ReadEmploymentTypeSchema,
    name="Update an employment type",
    description="This route is used to update an employment type on HRIS",
)
@inject
async def update_employment_type(
    employment_type_id: str,
    employment_type_data: UpdateEmploymentTypeSchema,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin", "manager", "hr"],
            required_permissions=[],
        )
    ),
):
    """Route to view an employee type on HRIS"""
    employment_type = await service.update_employment_type(employment_type_id, employment_type_data)

    return employment_type


@router.delete(
    "/employment-type/{employment_type_id}/delete",
    response_model=Optional[bool],
    name="Delete an employment type",
    description="This route is used to delete an employment type on HRIS",
)
@inject
async def delete_employment_type(
    employment_type_id: str,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin", "manager", "hr"],
            required_permissions=[],
        )
    ),
):
    """Route to view an employee type on HRIS"""
    employment_type = await service.delete_employment_type_by_id(employment_type_id,)

    return employment_type