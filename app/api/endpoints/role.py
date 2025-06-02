#!/usr/bin/env python3
# File: api/endpoints/role.py
# Author: Oluwatobiloba Light
"""Role endpoint"""

from typing import Sequence
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from app.core.container import Container
from app.schemas.role_schema import CreateRoleSchema, RoleSchema
from app.services.role_service import RoleService


router = APIRouter(
    prefix="/role",
    tags=["User Roles"],
)


@router.post(
    "/create",
    response_model=RoleSchema,
    name="Create a new role",
    description="This route is used to create a new role",
)
@inject
async def create_role(
    role: CreateRoleSchema,
    role_service: RoleService = Depends(Provide[Container.role_service]),
):
    """Route to create a new role"""
    new_role = await role_service.add_role(role)

    return new_role


@router.post(
    "/{role_id}/view",
    response_model=RoleSchema,
    name="Get a role by ID",
    description="This route is used to get a role by ID",
)
@inject
async def get_role_by_id(
    role_id: str,
    role_service: RoleService = Depends(Provide[Container.role_service]),
):
    """Route to create a new role"""
    existing_role = await role_service.get_by_id(role_id)

    return existing_role

@router.get("/all", response_model=Sequence[RoleSchema], name="Get all roles", description="This route is used to get all roles")
@inject
async def get_roles(
    role_service: RoleService = Depends(Provide[Container.role_service]),
):
    """Route to get all roles"""
    all_roles = await role_service.get_all()

    return all_roles