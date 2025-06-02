#!/usr/bin/env python3
# File: api/endpoints/auth.py
# Author: Oluwatobiloba Light
"""Auth endpoint"""

from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from app.core.container import Container
from app.schemas.auth_schema import LoginSchema, SignInResponse
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication & Authorization"],
)


@router.post(
    "/login",
    response_model=SignInResponse,
    name="Login as a user on HRIS",
    description="This route is used to login as a user on HRIS",
)
@inject
async def login(
    user_info: LoginSchema,
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    """Route to login as a user on HRIS"""
    user = await service.login(user_info)


    return user