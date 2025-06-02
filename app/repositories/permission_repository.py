#!/usr/bin/env python3
# File: repositories/permission_repository.py
# Author: Oluwatobiloba Light
"""Permission Repository"""

from uuid import UUID, uuid4
from sqlalchemy import select
from app.adapter.json_adapter import JSONAdapter
from app.adapter.sqlalchemy_adapter import SQLAlchemyAdapter
from app.models.permission import Permission
from app.models.role import Role
from app.schemas.permission_schema import CreatePermissionSchema
from typing import Optional, Sequence, TypeVar, Union
from psycopg2 import IntegrityError
from app.core.exceptions import (
    CustomDatabaseError,
    DuplicatedError,
    GeneralError,
    NotFoundError,
)
from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import (
    OperationalError,
    ProgrammingError,
    NoResultFound,
    StatementError,
)
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=Permission)


class PermissionRepository(BaseRepository):
    def __init__(self, db_adapter: Union[JSONAdapter, SQLAlchemyAdapter]):
        self.db_adapter = db_adapter
        self.model = Permission

        super().__init__(db_adapter, Permission)

    async def create(self, schema: CreatePermissionSchema) -> Permission:
        """Creates a new permission record"""
        roles = (
            await self.resolve_roles([role.model_dump() for role in schema.roles])
            if schema.roles and len(schema.roles) >= 1
            else []
        )

        query = self.model(roles=roles, **schema.model_dump(exclude=["roles"]))

        if isinstance(self.db_adapter, SQLAlchemyAdapter):
            async with self.db_adapter.session() as session, session.begin():
                try:
                    self.db_adapter.add(session, query)
                    await self.db_adapter.flush(session)
                    await self.db_adapter.refresh(session, query)

                    query_result = (
                        select(self.model)
                        .where(self.model.id == query.id)
                        .options(selectinload(self.model.roles))
                    )

                    query = (await session.execute(query_result)).scalar_one()
                except IntegrityError as e:
                    await self.db_adapter.rollback(session)
                    raise CustomDatabaseError(message=str(e), original_exception=e)
                except Exception as e:
                    if "duplicate" in str(e).lower():
                        error_msg = "Permission already exists!"
                        # raise error_msg
                        raise DuplicatedError(detail=error_msg)
                    else:
                        print(f"Other integrity error: {str(e)}")
                        raise GeneralError(detail=str(e))
                else:
                    await self.db_adapter.commit(session)
        elif isinstance(self.db_adapter, JSONAdapter):
            query.id = str(uuid4())
            self.db_adapter.add("roles", query.model_dump(exclude_none=True))

        return query

    async def get_by_id(self, id: UUID) -> Union[Permission, None]:
        """Get a permission record from the database by ID"""
        query = (
            select(self.model)
            .where(self.model.id == id)
            .options(
                selectinload(self.model.roles),
                selectinload(self.model.users),
                     )
        )

        async with self.db_adapter.session() as session, session.begin():
            try:
                result = (await session.execute(query)).scalar_one_or_none()

                return result
            except OperationalError as e:
                logger.error("Operational error (e.g., DB connection issue): %s", e)
                raise CustomDatabaseError(
                    message="Something happened with the database connectivity"
                )

            except ProgrammingError as e:
                logger.error("Programming error (e.g., invalid column/table): %s", e)
                raise CustomDatabaseError(message=str(e))

            except NoResultFound as e:
                logger.warning("No result found where one was expected: %s", e)
                raise NotFoundError(detail="Permission does not exist or ID is invalid")

            except StatementError as e:
                logger.error(
                    "Statement error (e.g., type mismatch or bad query): %s", e
                )
                raise CustomDatabaseError(
                    message="An error occured executing query statement"
                )

            except AttributeError as e:
                logger.error("Model attribute error: %s", e)
                raise GeneralError(detail="Model attribute error")

            except TypeError as e:
                logger.error("Type error in select/model usage: %s", e)
                raise GeneralError(detail="Type error ")

        return None

    async def get_all(self) -> Sequence[Permission]:
        """Gets all permission records from the database"""
        async with self.db_adapter.session() as session, session.begin():
            try:
                query = select(self.model).options(selectinload(self.model.roles))

                result = (await session.execute(query)).scalars().all()

                return result
            except Exception as e:
                raise GeneralError(detail=str(e))

    async def resolve_roles(self, role_data: list[dict]) -> list[Role]:
        """Resolves a role"""
        return [(await self.get_or_create_role(d["name"])) for d in role_data]

    async def get_or_create_role(self, name: str) -> Role:
        """Creates or returns an existing role record from the database"""
        from app.models.role import Role

        query = select(Role).where(Role.name == name)

        async with self.db_adapter.session() as session, session.begin():
            try:
                existing = (await session.execute(query)).scalars().first()

                if existing:
                    return existing

                new_dest = Role(name=name)
                await self.db_adapter.add(session, new_dest)
                await self.db_adapter.flush(session)
                await self.db_adapter.refresh(session, new_dest)

            except IntegrityError as e:
                await self.db_adapter.rollback(session)
                raise DuplicatedError(detail=str(e.orig))
            except Exception as e:
                if "duplicate" in str(e).lower():
                    print(str(e))
                    error_msg = "This tour package '{}' exists!".format(query.title)
                    raise DuplicatedError(detail=error_msg)
                else:
                    print(f"Other integrity error: {str(e)}")
                    raise DuplicatedError(detail=str(e))
            else:
                await self.db_adapter.commit(session)

            return new_dest

    async def get_by_name(self, name: str) -> Optional[Permission]:
        """Get a permission by name"""
        async with self.session_scope() as session:
            result = await session.execute(select(self.model).where(self.model.name == name))
            return result.scalars().first()