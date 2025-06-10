#!/usr/bin/env python3
# File: api/endpoints/department.py
# Author: Oluwatobiloba Light
"""Department endpoint"""

from typing import Optional, Sequence
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from app.core.container import Container
from app.core.dependencies import require_roles_and_permissions
from app.models.user import User
from app.schemas.department_schema import (
    AssignDepartmentTeamLeadSchema,
    CreateDepartmentSchema,
    CreateUserDepartmentSchema,
    ReadDepartmentSchema,
    UpdateDepartmentSchema,
)
from app.services.department_service import DepartmentService


router = APIRouter(
    prefix="/department",
    tags=["Department Management"],
)


@router.post(
    "/create",
    response_model=ReadDepartmentSchema,
    name="Create a new department",
    description="This route is used to create a new department",
)
@inject
async def create_department(
    department: CreateDepartmentSchema,
    department_service: DepartmentService = Depends(
        Provide[Container.department_service]
    ),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin"],
            # required_permissions=["*"],
        )
    ),
):
    """Route to create a new department"""
    new_department = await department_service.create_department(department)

    return new_department


@router.post(
    "/team-lead/assign",
    response_model=ReadDepartmentSchema,
    name="Assigns a team lead to a department",
    description="This route is used to assign a team lead to a department",
)
@inject
async def assign_team_lead_to_department(
    data: AssignDepartmentTeamLeadSchema,
    department_service: DepartmentService = Depends(
        Provide[Container.department_service]
    ),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin"],
            required_permissions=["full_access"],
        )
    ),
):
    """Route to assign a team lead to a department"""
    result = await department_service.assign_team_lead(
        data.team_lead_id, data.department_id
    )

    return result


@router.get(
    "/all",
    response_model=Sequence[ReadDepartmentSchema],
    name="View all departments",
    description="This route is used to view all departments",
)
@inject
async def view_departments(
    department_service: DepartmentService = Depends(
        Provide[Container.department_service]
    ),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin", "manager", "hr"],
            required_permissions=[],
        )
    ),
):
    """Route to view all departments"""
    departments = await department_service.get_all_departments()

    return departments


@router.get(
    "/{department_id}/view",
    response_model=ReadDepartmentSchema,
    name="View a department",
    description="This route is used to view a department",
)
@inject
async def view_department(
    department_id: str,
    department_service: DepartmentService = Depends(
        Provide[Container.department_service]
    ),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin", "manager", "hr"],
            required_permissions=[],
        )
    ),
):
    """Route to view all departments"""
    department = await department_service.get_department_by_id(department_id)

    return department


@router.post(
    "/team-member/assign",
    response_model=Optional[ReadDepartmentSchema],
    name="Assigns a team member to a department",
    description="This route is used to assign a team member to a department",
)
@inject
async def assign_team_member_to_department(
    data: CreateUserDepartmentSchema,
    department_service: DepartmentService = Depends(
        Provide[Container.department_service]
    ),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin"],
            required_permissions=["all", "can_edit_department"],
        )
    ),
):
    """Route to assign a team lead to a department"""
    result = await department_service.assign_team_member(
        data.user_id, data.department_id
    )

    return result


@router.patch(
    "/{department_id}/edit",
    response_model=Optional[ReadDepartmentSchema],
    name="Update a department by ID",
    description="This route is used to update a department by ID",
)
@inject
async def update_department(
    department_id: str,
    data: UpdateDepartmentSchema,
    department_service: DepartmentService = Depends(
        Provide[Container.department_service]
    ),
    current_user: User = Depends(
        require_roles_and_permissions(
            required_roles=["super_admin", "hr", "manager"],
            required_permissions=[],
        )
    ),
):
    """Route to assign a team lead to a department"""
    print("data", data)
    result = await department_service.update_department_by_id(department_id, data)

    return result
