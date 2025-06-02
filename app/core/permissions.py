from app.enums import UserRoleType

ROLE_DEFAULT_PERMISSIONS = {
    UserRoleType.EMPLOYEE: {"read_self_profile", "edit_self_profile", "submit_leave_request"},
    UserRoleType.HR: {"view_all_employees", "approve_leave_request"},
    UserRoleType.MANAGER: {"manage_team", "approve_team_leave"},
    UserRoleType.ADMIN: {"view_all", "manage_users", "manage_permissions"},
    UserRoleType.SUPER_ADMIN: {"*"},  # wildcard for all permissions
}
