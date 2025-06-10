#!/usr/bin/env python3
# File: app/api/routes.py
# Author: Oluwatobiloba Light
"""Routes File"""


from fastapi import APIRouter
from app.api.endpoints.attendance import router as attendance_router
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.department import router as department_router
from app.api.endpoints.leave import router as leave_router
from app.api.endpoints.role import router as role_router
from app.api.endpoints.permission import router as permission_router
from app.api.endpoints.admin import router as admin_router
from app.api.endpoints.bank import router as bank_router
from app.api.endpoints.payroll import router as payroll_router
from app.api.endpoints.pension import router as pension_router

routers = APIRouter()

router_list = [
    attendance_router,
    auth_router,
    department_router,
    leave_router,
    role_router,
    permission_router,
    admin_router,
    bank_router,
    payroll_router,
    pension_router,
]

for router in router_list:
    routers.include_router(router)
