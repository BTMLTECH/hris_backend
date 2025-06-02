#!/usr/bin/env python3
# File: services/leave_service.py
# Author: Oluwatobiloba Light
"""Leave Services"""


from datetime import datetime
from app.models.leave_approver import LeaveApprover
from app.models.leave_reliever import LeaveReliever
from app.models.leave_request import LeaveRequest, LeaveRequestType
from app.models.user import User
from app.repositories.leave_approver_repository import LeaveApproverRepository
from app.repositories.leave_reliever_repository import LeaveRelieverRepository
from app.repositories.leave_request_repository import LeaveRequestRepository
from app.repositories.supervisor_repository import UserSupervisorRepository
from app.schemas.leave_schema import CreateLeaveRequestSchema
from app.core.exceptions import GeneralError
import logging


logger = logging.getLogger(__name__)


class LeaveRequestService:
    def __init__(
        self,
        leave_request_repository: LeaveRequestRepository,
        leave_approver_repository: LeaveApproverRepository,
        leave_reliever_repository: LeaveRelieverRepository,
        user_supervisor_repository: UserSupervisorRepository,
    ):
        self.leave_request_repository = leave_request_repository
        self.leave_approver_repository = leave_approver_repository
        self.leave_reliever_repository = leave_reliever_repository
        self.user_supervisor_repository = user_supervisor_repository

    async def create_leave_request(
        self, user: User, schema: CreateLeaveRequestSchema
    ) -> LeaveRequest:
        try:
            # Create the leave request record
            leave_request = await self.leave_request_repository.create(schema)

            print(leave_request)

            # 2. Load supervisors from UserSupervisor
            supervisors = (
                await self.user_supervisor_repository.get_supervisors_for_user(user.id)
            )

            # 3. Determine approvers by role
            approvers = []
            user_roles = [role for role in user.roles]  # Assuming roles are preloaded

            step_order = {"TEAM_LEAD": 1, "HR": 2, "MD": 3}

            if "EMPLOYEE" in user_roles:
                required_roles = ["TEAM_LEAD", "HR"]
            elif "TEAM_LEAD" in user_roles:
                required_roles = ["HR"]
            elif "HR" in user_roles:
                required_roles = ["MD"]
            # elif "MD" in user_roles or "SUPER_ADMIN" in user_roles:
            #     # Optional: auto-approve
            #     leave_request.status = LeaveRequestType.APPROVED
            #     await self.leave_request_repository.update_by_id(
            #         leave_request.id, leave_request
            #     )
            #     required_roles = []
            else:
                raise GeneralError("Unsupported user role for leave request")

            # 4. Create LeaveApprover records
            for supervisor in supervisors:
                role = supervisor.role.upper()
                if role in required_roles:
                    approver = LeaveApprover(
                        leave_request_id=leave_request.id,
                        approver_id=supervisor.supervisor_id,
                        role=role,
                        step=step_order.get(role, 99),
                    )
                    await self.leave_approver_repository.create(approver)

            # 5. Create LeaveReliever records
            for reliever_id in schema.reliever_ids:
                reliever = LeaveReliever(
                    leave_request_id=leave_request.id,
                    reliever_id=reliever_id,
                    leave_request=leave_request,
                )
                await self.leave_reliever_repository.create(reliever)

            return leave_request
        except Exception as e:
            logger.error(f"An error has occured while requesting for leave {e}")
            raise GeneralError("Failed to create leave request") from e
