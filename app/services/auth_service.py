#!/usr/bin/env python3
# File: app/services/auth_service.py
# Author: Oluwatobiloba Light
"""Authentication Services"""

from datetime import datetime, timedelta
import logging
import secrets
from typing import Optional
from uuid import UUID
from app.core.config import hris_config
from fastapi import HTTPException, status
from app.core.exceptions import UnauthorizedError
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import LoginSchema, Payload
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models import User
from app.services.base_service import BaseService

logger = logging.getLogger(__name__)


class AuthService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

        super().__init__(user_repository)

    async def login(self, schema: LoginSchema):
        user = await self.user_repository.get_by_email(schema.email)

        if not user:
            raise UnauthorizedError(detail="Incorrect email or password")

        if (user.password and schema.password) and not verify_password(
            schema.password, user.password
        ):
            raise UnauthorizedError(detail="Incorrect email or password")

        if not user.is_active:
            raise UnauthorizedError(detail="Account is not active!")

        delattr(user, "password")

        payload = Payload(
            id=str(user.id),
            name=user.first_name + " " + user.last_name,
            email=user.email,
            role=user.role,
        )

        token_lifespan = timedelta(minutes=30000)

        access_token, expiration_datetime = create_access_token(
            payload.model_dump(), token_lifespan
        )

        await self.user_repository.update_by_id(
            user.id, {"last_login_at": datetime.now()}
        )

        csrf_token = secrets.token_hex(32)

        # (cache user result to redis - coming soon!)
        # user_data = {
        #     "id": str(user.id),
        #     "created_at": str(user.created_at),
        #     "updated_at": str(user.updated_at),
        #     "last_login_at": str(user.last_login_at),
        #     **user.model_dump(
        #         exclude=[
        #             "id",
        #             "created_at",
        #             "updated_at",
        #             "deleted_at",
        #             "last_login_at",
        #         ]
        #     ),
        #     "csrf_token": csrf_token,
        #     "access_token": access_token,
        # }

        # await self.redis_service.cache_data(f"user:{user.id}", user_data)
        login_result = {
            "access_token": access_token,
            "csrf_token": csrf_token,
            "user": user,
        }

        return login_result
