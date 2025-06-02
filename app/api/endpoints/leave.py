#!/usr/bin/env python3
# File: api/endpoints/leave.py
# Author: Oluwatobiloba Light
"""Leave endpoint"""

from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from app.core.container import Container
from app.schemas.leave_schema import CreateLeaveRequestSchema, ReadLeaveRequestSchema
from app.services.leave_service import LeaveRequestService


router = APIRouter(
    prefix="/leave-request",
    tags=["Leave Management"],
)


@router.post(
    "/create",
    response_model=ReadLeaveRequestSchema,
    name="Create a new leave request",
    description="This route is used to create a new leave request",
)
@inject
async def create_leave(
    leave: CreateLeaveRequestSchema,
    leave_service: LeaveRequestService = Depends(Provide[Container.leave_request_service]),
):
    """Route to create a new leave"""
    new_leave = await leave_service.create_leave_request(leave)

    return new_leave
