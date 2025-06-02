#!/usr/bin/env python3
# File: api/endpoints/permission.py
# Author: Oluwatobiloba Light
"""Permission endpoint"""

from typing import Sequence
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from app.core.container import Container
from app.schemas.permission_schema import CreatePermissionSchema, PermissionSchema
from app.services.permission_service import PermissionService


router = APIRouter(
    prefix="/permission",
    tags=["User Permissions"],
)


@router.post(
    "/create",
    response_model=PermissionSchema,
    name="Create a new user permission",
    description="This route is used to create a new permission",
)
@inject
async def create_permission(
    permission: CreatePermissionSchema,
    permission_service: PermissionService = Depends(Provide[Container.permission_service]),
):
    """Route to create a new permission"""
    new_permission = await permission_service.add_permission(permission)

    return new_permission


@router.post(
    "/{permission_id}/view",
    response_model=PermissionSchema,
    name="Get a permission by ID",
    description="This route is used to get a permission by ID",
)
@inject
async def get_permission_by_id(
    permission_id: str,
    permission_service: PermissionService = Depends(Provide[Container.permission_service]),
):
    """Route to create a new permission"""
    existing_permission = await permission_service.get_by_id(permission_id)

    return existing_permission

@router.get("/all", response_model=Sequence[PermissionSchema], name="Get all permissions", description="This route is used to get all permissions")
@inject
async def get_permissions(
    permission_service: PermissionService = Depends(Provide[Container.permission_service]),
):
    """Route to get all permissions"""
    all_permissions = await permission_service.get_all()

    return all_permissions