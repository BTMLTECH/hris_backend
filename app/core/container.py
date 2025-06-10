#!/usr/bin/env python3
# File: app/core/container.py
# Author: Oluwatobiloba Light
"""HRIS Dependency Container"""

from dependency_injector import containers, providers
from app.adapter.cache.redis_adapter import RedisAdapter
from app.core.database import Database, RedisConnection
from app.adapter.json_adapter import JSONAdapter
from app.adapter.sqlalchemy_adapter import SQLAlchemyAdapter
from app.core.config import hris_config
from app.repositories import *
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.bank_repository import BankRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.payroll_repository import PayrollRepository
from app.repositories.pension_repository import PensionRepository
from app.repositories.permission_repository import PermissionRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_department_repository import UserDepartmentLinkRepository
from app.repositories.user_repository import UserRepository
from app.services.attendance_service import AttendanceService
from app.services.auth_service import AuthService
from app.services.bank_service import BankService
from app.services.department_service import DepartmentService
from app.services.leave_service import LeaveRequestService
from app.services.payroll_service import PayrollService
from app.services.pension_service import PensionService
from app.services.permission_service import PermissionService
from app.services.role_service import RoleService
from app.services.user_service import UserService
from app.repositories.leave_request_repository import LeaveRequestRepository
from app.repositories.leave_approver_repository import LeaveApproverRepository
from app.repositories.leave_reliever_repository import LeaveRelieverRepository
from app.repositories.supervisor_repository import UserSupervisorRepository


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.endpoints.admin",
            "app.api.endpoints.attendance",
            "app.api.endpoints.auth",
            "app.api.endpoints.bank",
            "app.api.endpoints.department",
            "app.api.endpoints.leave",
            "app.api.endpoints.role",
            "app.api.endpoints.payroll",
            "app.api.endpoints.pension",
            "app.api.endpoints.permission",
            "app.core.dependencies",
        ]
    )
    config = providers.Configuration()

    db = providers.Singleton(
        Database,
        db_url=(
            hris_config.DATABASE_URI
            if hris_config.ENV == "production"
            else hris_config.DATABASE_LOCAL_URI
        ),
    )

    # Database and Cache Adapters
    # database_adapter = providers.Selector(
    #     bool(hris_config.USE_DATABASE),
    #     true=providers.Factory(SQLAlchemyAdapter, session=db.provided.session),
    #     false=providers.Factory(JSONAdapter, file_path="db.json"),
    # )

    database_adapter = (
        providers.Factory(SQLAlchemyAdapter, session=db.provided.session)
        if hris_config.USE_DATABASE == "true"
        else providers.Factory(JSONAdapter, file_path="db.json")
    )

    redis_client = providers.Singleton(
        RedisConnection,
        host="localhost" if hris_config.ENV == "dev" else hris_config.REDIS_URL,
        port=6379 if hris_config.ENV == "dev" else hris_config.REDIS_PORT,
        db=0,
    )

    redis_adapter = providers.Factory(
        RedisAdapter, client=redis_client.provided.connection
    )

    # Repositories
    attendance_repository = providers.Factory(
        AttendanceRepository, db_adapter=database_adapter
    )
    auth_repository = providers.Factory(UserRepository, db_adapter=database_adapter)
    bank_repository = providers.Factory(BankRepository, db_adapter=database_adapter)
    department_repository = providers.Factory(
        DepartmentRepository, db_adapter=database_adapter
    )
    payroll_repository = providers.Factory(
        PayrollRepository, db_adapter=database_adapter
    )
    pension_repository = providers.Factory(
        PensionRepository, db_adapter=database_adapter
    )
    permission_repository = providers.Factory(
        PermissionRepository, db_adapter=database_adapter
    )
    role_repository = providers.Factory(RoleRepository, db_adapter=database_adapter)
    user_repository = providers.Factory(UserRepository, db_adapter=database_adapter)

    leave_request_repository = providers.Factory(
        LeaveRequestRepository, db_adapter=database_adapter
    )
    leave_approver_repository = providers.Factory(
        LeaveApproverRepository, db_adapter=database_adapter
    )
    leave_reliever_repository = providers.Factory(
        LeaveRelieverRepository, db_adapter=database_adapter
    )

    user_department_repository = providers.Factory(
        UserDepartmentLinkRepository, db_adapter=database_adapter
    )

    user_supervisor_repository = providers.Factory(
        UserSupervisorRepository, db_adapter=database_adapter
    )

    # Services
    attendance_service = providers.Factory(AttendanceService, attendance_repository)
    auth_service = providers.Factory(AuthService, user_repository)
    bank_service = providers.Factory(BankService, bank_repository)
    department_service = providers.Factory(
        DepartmentService, department_repository, user_department_repository
    )

    leave_request_service = providers.Factory(
        LeaveRequestService,
        leave_request_repository=leave_request_repository,
        leave_approver_repository=leave_approver_repository,
        leave_reliever_repository=leave_reliever_repository,
        user_supervisor_repository=user_supervisor_repository,
    )
    payroll_service = providers.Factory(PayrollService, payroll_repository)
    pension_service = providers.Factory(PensionService, pension_repository)
    permission_service = providers.Factory(PermissionService, permission_repository)
    role_service = providers.Factory(RoleService, role_repository)
    user_service = providers.Factory(
        UserService,
        user_repository,
        role_repository,
        permission_repository,
        department_repository,
    )
