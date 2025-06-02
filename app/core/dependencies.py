#!/usr/bin/env python3
# File: dependencies.py
# Author: Oluwatobiloba Light
"""Dependencies"""


from typing import List
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from jose import jwt, JWTError
from pydantic import ValidationError
from app.core.config import hris_config
from app.core.container import Container
from app.core.exceptions import GeneralError, UnauthorizedError
from app.core.security import ALGORITHM, JWTBearer
from app.models.user import User
from app.schemas.auth_schema import Payload
from app.services.user_service import UserService


@inject
async def get_current_user(
    # csrf_token_cookie: str = Depends(CookieBearer()),
    token: str = Depends(JWTBearer()),
    user_service: UserService = Depends(Provide[Container.user_service]),
    # redis_service: RedisService = Depends(Provide[Container.redis_service]),
) -> User:

    try:
        payload = jwt.decode(token, hris_config.SECRET_KEY, algorithms=ALGORITHM)

        token_data = Payload(**payload)

        # redis_data = await redis_service.retrieve_data(f"user:{token_data.id}")

        # current_user: Union[User, None] = None
        current_user = await user_service.get_by_id(token_data.id)

        # if not redis_data:
        #     current_user = await user_service.get_by_id(token_data.id)

        #     user_data = {
        #         "id": str(current_user.id),
        #         "created_at": str(current_user.created_at),
        #         "updated_at": str(current_user.updated_at),
        #         "last_login_at": str(current_user.last_login_at),
        #         **current_user.model_dump(
        #             exclude=[
        #                 "id",
        #                 "created_at",
        #                 "updated_at",
        #                 "deleted_at",
        #                 "last_login_at",
        #             ]
        #         ),
        #         # "csrf_token": "csrf_token_cookie",
        #         "access_token": token,
        #     }

        #     await redis_service.cache_data(f"user:{current_user.id}", user_data)
        #     return current_user
        # else:
        #     user_data = json.loads(redis_data)

        #     # if user_data["csrf_token"] != csrf_token_header:
        #     #     raise AuthForbiddenError(
        #     #         detail="Could not validate credentials")

        #     user = CachedUser(**user_data)

        #     return User(**user.model_dump())
        return current_user
    except (JWTError, ValidationError) as e:
        raise UnauthorizedError(detail="Could not validate credentials") from e


async def is_user_admin(current_user: User = Depends(get_current_user)):
    """Checks if user is an admin"""
    if not current_user.is_active:
        raise UnauthorizedError("Inactive user")
    if not current_user.is_admin:
        raise UnauthorizedError("User is not an admin!")
    return current_user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise UnauthorizedError("Inactive user")
    return current_user


@inject
def require_roles_and_permissions(
    required_roles: List[str] = [],
    required_permissions: List[str] = [],
):
    @inject
    async def dependency(
        current_user: User = Depends(get_current_user),
        user_service: UserService = Depends(Provide[Container.user_service]),
    ):
        # available_roles = {
        #     "super_admin",
        #     "admin",
        #     "hr_admin",
        #     "department_admin",
        #     "employee",
        # }

        if not current_user:
            raise GeneralError(detail="You are unauthorized", status_code=401)

        user = await user_service.get_by_id(
            str(current_user.id),
        )

        if not user or not user.role:
            raise UnauthorizedError("User has no role assigned.")

        if required_roles:
            user_role_name = user.role.name.lower()
            if user_role_name not in [r.lower() for r in required_roles]:
                raise UnauthorizedError(
                    f"Requires one of these roles: {required_roles}"
                )

        if required_permissions:
            user_permission_names = (
                [permission.name for permission in user.permissions]
                if user.permissions and len(user.permissions) > 0
                else []
            )

            missing = [p in user_permission_names for p in required_permissions]

            if not any(missing):
                raise UnauthorizedError(
                    f"User does not have these permissions: {missing}"
                )

        return user

    return dependency
