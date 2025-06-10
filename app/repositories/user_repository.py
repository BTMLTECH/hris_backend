#!/usr/bin/env python3
# File: app/repositories/user_repository.py
# Author: Oluwatobiloba Light
"""User Repository"""

from uuid import uuid4
from pydantic import EmailStr
from app.adapter.json_adapter import JSONAdapter
from app.adapter.sqlalchemy_adapter import SQLAlchemyAdapter
from app.core.security import get_password_hash
from app.models.employment_type import EmploymentType
from app.models.role import Role
from app.models.user_permission import UserPermissionLink
from app.models.user_role import UserRoleLink
from app.schemas.auth_schema import (
    UserSignUpSchema,
)
from app.models.user import User
from typing import Sequence, TypeVar, Union
from psycopg2 import IntegrityError
from sqlalchemy import UUID, select, update
from app.core.exceptions import CustomDatabaseError, GeneralError, NotFoundError
from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import selectinload
import logging
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.user_schema import (
    CreateEmploymentTypeSchema,
    ReadEmploymentTypeSchema,
    UpdateEmploymentTypeSchema,
    UserUpdateSchema,
)
from sqlalchemy.exc import (
    OperationalError,
    ProgrammingError,
    NoResultFound,
    StatementError,
)

logger = logging.getLogger(__name__)


T = TypeVar("T", bound=User)


class UserRepository(BaseRepository):
    def __init__(self, db_adapter: Union[JSONAdapter, SQLAlchemyAdapter]):
        self.db_adapter = db_adapter
        self.model = User

        super().__init__(db_adapter, User)

    # async def create(self, schema: CreateUserSchema) -> User:
    #     """Creates a new user"""
    #     schema.password = get_password_hash(schema.password)
    #     query = self.model(**schema.model_dump(exclude_none=True))

    #     if isinstance(self.db_adapter, SQLAlchemyAdapter):
    #         async with self.db_adapter.session() as session, session.begin():
    #             try:
    #                 self.db_adapter.add(session, query)
    #                 await self.db_adapter.flush(session)
    #                 await self.db_adapter.refresh(session, query)
    #             except IntegrityError as e:
    #                 await self.db_adapter.rollback(session)
    #                 raise DuplicatedError(detail=str(e.orig))
    #             except Exception as e:
    #                 if "duplicate" in str(e).lower():
    #                     error_msg = "An account with that email address exists!"
    #                     raise DuplicatedError(detail=error_msg)
    #                 else:
    #                     print(f"Other integrity error: {str(e)}")
    #                     raise DuplicatedError(detail=str(e))
    #             else:
    #                 await self.db_adapter.commit(session)
    #     elif isinstance(self.db_adapter, JSONAdapter):
    #         query.id = str(uuid4())
    #         self.db_adapter.add("users", query.model_dump(exclude_none=True))

    #     return query

    async def create(self, schema: UserSignUpSchema) -> User:
        """Creates a new user"""
        if isinstance(self.db_adapter, SQLAlchemyAdapter):
            async with self.session_scope() as session:
                try:
                    # Ensure password is hashed
                    schema.password = get_password_hash(schema.password)
                    new_user = self.model(
                        role=schema.role,
                        permissions=schema.permissions,
                        next_of_kin=schema.next_of_kin,
                        **schema.model_dump(
                            exclude_none=True,
                            exclude=[
                                "role",
                                "permissions",
                                "user_role",
                                "user_permissions",
                                "next_of_kin",
                                "bank",
                            ],
                        ),
                    )

                    session.add(new_user)
                    await session.flush(
                        session,
                    )
                    await session.refresh(new_user)

                    query = (
                        await session.execute(
                            select(self.model)
                            .where(self.model.email == schema.email)
                            .options(
                                selectinload(self.model.role).selectinload(
                                    Role.permissions
                                ),
                                selectinload(self.model.next_of_kin),
                                selectinload(self.model.permissions),
                                selectinload(self.model.bank),
                                selectinload(self.model.attendance),
                                selectinload(self.model.department),
                                selectinload(self.model.leave_requests),
                                selectinload(self.model.employment_type),
                                selectinload(self.model.payroll_class),
                                selectinload(self.model.pension),
                            )
                        )
                    ).scalar_one()

                    new_user = query

                    return new_user
                except IntegrityError as e:
                    logger.error("Integrity error during user creation: %s", e)
                    raise e
                except Exception as e:
                    logger.error("Unexpected error during user creation: %s", e)
                    raise e

        elif isinstance(self.db_adapter, JSONAdapter):
            query.id = str(uuid4())
            self.db_adapter.add("users", query.model_dump(exclude_none=True))

    async def create_employment_type(
        self, schema: CreateEmploymentTypeSchema
    ) -> EmploymentType:
        """Create employment type record in the DB"""
        async with self.session_scope() as session:
            from app.models.employment_type import EmploymentType

            try:
                new_employment_type = EmploymentType(
                    **schema.model_dump(
                        exclude_none=True,
                    )
                )

                session.add(new_employment_type)
                await session.flush(
                    session,
                )

                await session.refresh(new_employment_type)

                query = (
                    await session.execute(
                        select(EmploymentType).where(
                            EmploymentType.id == new_employment_type.id
                        )
                    )
                ).scalar_one()

                new_employment_type = query

                return new_employment_type
            except IntegrityError as e:
                logger.error("Integrity error during creation: %s", e)
                raise e
            except Exception as e:
                logger.error("Unexpected error during creation: %s", e)
                raise e

    async def get_all_employment_types(self) -> Sequence[ReadEmploymentTypeSchema]:
        """Get all employment types records from the database"""
        async with self.db_adapter.session() as session, session.begin():
            from app.models.employment_type import EmploymentType

            try:
                query = select(EmploymentType)

                query = (await session.execute(query)).scalars().all()
                return query
            except Exception as e:
                logger.error("An error has occured {}".format(e))
                raise

    async def update_employment_type_by_id(
        self, id: UUID, employment_type_fields: UpdateEmploymentTypeSchema
    ) -> EmploymentType:
        """Update an employment type record in the database by ID"""
        try:
            async with self.session_scope() as session:
                query = (
                    update(EmploymentType)
                    .where(EmploymentType.id == id)
                    .values({**employment_type_fields.model_dump(exclude_none=True)})
                    .execution_options(synchronize_session="fetch")
                )

                result = await session.execute(query)

                updated_record = (
                    await session.execute(
                        select(EmploymentType).where(EmploymentType.id == id)
                    )
                ).scalar_one_or_none()

                if result.rowcount < 1:
                    return updated_record

                return updated_record
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
            raise NotFoundError(detail="Bank does not exist or ID is invalid")

        except StatementError as e:
            logger.error("Statement error (e.g., type mismatch or bad query): %s", e)
            raise CustomDatabaseError(
                message="An error occured executing query statement"
            )

        except AttributeError as e:
            logger.error("Model attribute error: %s", e)
            raise GeneralError(detail="Model attribute error")

        except TypeError as e:
            logger.error("Type error in select/model usage: %s", e)
            raise GeneralError(detail="Type error ")

    async def get_employment_type_by_id(self, id: UUID):
        """Get employment type record by ID"""
        query = select(EmploymentType).where(EmploymentType.id == id)

        try:
            async with self.db_adapter.session() as session, session.begin():
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
            raise NotFoundError(detail="Employment type does not exist or ID is invalid")

        except StatementError as e:
            logger.error("Statement error (e.g., type mismatch or bad query): %s", e)
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

    async def delete_employment_type_by_id(self, id: UUID) -> bool:
        try:
            async with self.session_scope() as session:
                employmnt_type = (
                    await session.execute(
                        select(EmploymentType).where(EmploymentType.id == id)
                    )
                ).scalar_one_or_none()

                if not employmnt_type:
                    return False

                await session.delete(employmnt_type)
                await session.commit()
                return True
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
            raise NotFoundError(
                detail="Employment Type does not exist or ID is invalid"
            )

        except StatementError as e:
            logger.error("Statement error (e.g., type mismatch or bad query): %s", e)
            raise CustomDatabaseError(
                message="An error occured executing query statement"
            )

        except AttributeError as e:
            logger.error("Model attribute error: %s", e)
            raise GeneralError(detail="Model attribute error")

        except TypeError as e:
            logger.error("Type error in select/model usage: %s", e)
            raise GeneralError(detail="Type error ")

    async def update(
        self, schema: T, updated_fields: dict[str, any]
    ) -> Union[User, None]:
        """Updte user record in the DB"""
        async with self.db_adapter.session() as session, session.begin():
            query = (
                update(self.model)
                .where(self.model.email == schema.email)
                .values(**updated_fields)
                .execution_options(synchronize_session="fetch")
            )

            try:
                result = await session.execute(query)

                q = select(self.model).where(self.model.email == schema.email)

                updated_record = (await session.execute(q)).scalar_one_or_none()

                if result.rowcount < 1:
                    return updated_record

                return updated_record
            except Exception as e:
                await self.db_adapter.rollback(session)
                raise e
            except:
                raise

    async def get_by_email(
        self, email: EmailStr, eager: bool = False
    ) -> Union[User, None]:
        """
        Get a user by their email
        """
        async with self.db_adapter.session() as session, session.begin():
            try:
                query = (
                    select(self.model)
                    .where(self.model.email == email)
                    .options(
                        selectinload(self.model.role).selectinload(Role.permissions),
                        selectinload(self.model.next_of_kin),
                        selectinload(self.model.permissions),
                        selectinload(self.model.bank),
                        selectinload(self.model.attendance),
                        selectinload(self.model.department),
                        selectinload(self.model.leave_requests),
                        selectinload(self.model.employment_type),
                        selectinload(self.model.payroll_class),
                        selectinload(self.model.pension),
                    )
                )

                query = (await session.execute(query)).scalar()

                if query is None:
                    return None

                return query
            except Exception as e:
                print("An error has occured", e)
                raise e

    async def get_by_id(self, id: UUID) -> Union[User, None]:
        """Get a user by id"""
        if isinstance(self.db_adapter, SQLAlchemyAdapter):
            async with self.db_adapter.session() as session, session.begin():
                try:
                    query = (
                        select(self.model)
                        .where(self.model.id == id)
                        .options(
                            selectinload(self.model.role).selectinload(
                                Role.permissions
                            ),
                            selectinload(self.model.next_of_kin),
                            selectinload(self.model.permissions),
                            selectinload(self.model.bank),
                            selectinload(self.model.attendance),
                            selectinload(self.model.department),
                            selectinload(self.model.leave_requests),
                            selectinload(self.model.employment_type),
                            selectinload(self.model.payroll_class),
                            selectinload(self.model.pension),
                        )
                    )

                    query = (await session.execute(query)).scalar_one_or_none()

                    print("query")

                    return query
                except Exception as e:
                    print("An error has occured", e)
                    raise e
        elif isinstance(self.db_adapter, JSONAdapter):
            return await self.db_adapter.get_by_id("users", str(id))

    async def delete_by_id(self, id: UUID) -> Union[User, None]:
        """Delete a user by id"""
        try:
            async with self.db_adapter.session() as session, session.begin():
                user = (
                    await session.execute(select(self.model).where(self.model.id == id))
                ).scalar_one_or_none()

                if not user:
                    return False

                await session.delete(user)
                await session.commit()
                return True
        except SQLAlchemyError as e:
            logger.error(f"Error deleting user with id {id}: {e}")
            return e

    async def activate_user(self, id: UUID):
        """Activates an employee"""
        try:
            async with self.session_scope() as session:
                result = await session.execute(
                    update(self.model)
                    .where(self.model.id == id)
                    .values({"is_active": True})
                    .execution_options(synchronize_session="fetch")
                )

                q = select(self.model).where(self.model.id == id)

                updated_record = (await session.execute(q)).scalar_one_or_none()

                if result.rowcount < 1:
                    return updated_record

                print("shshs", updated_record.is_active)

                return updated_record
        except SQLAlchemyError as e:
            raise e
        except Exception as e:
            raise e

    async def deactivate_user(self, id: UUID):
        """Deactivates an employee"""
        try:
            async with self.session_scope() as session:
                result = await session.execute(
                    update(self.model)
                    .where(self.model.id == id)
                    .values({"is_active": False})
                    .execution_options(synchronize_session="fetch")
                )

                q = select(self.model).where(self.model.id == id)

                updated_record = (await session.execute(q)).scalar_one_or_none()

                if result.rowcount < 1:
                    return updated_record

                print("shshs", updated_record.is_active)

                return updated_record
        except SQLAlchemyError as e:
            raise e
        except Exception as e:
            raise e

    async def get_all(self) -> Sequence[User]:
        """Get all users"""
        async with self.db_adapter.session() as session, session.begin():
            try:
                query = select(self.model).options(
                    selectinload(self.model.role).selectinload(Role.permissions),
                    selectinload(self.model.next_of_kin),
                    selectinload(self.model.permissions),
                    selectinload(self.model.bank),
                    selectinload(self.model.attendance),
                    selectinload(self.model.department),
                    selectinload(self.model.leave_requests),
                    selectinload(self.model.employment_type),
                    selectinload(self.model.payroll_class),
                    selectinload(self.model.pension),
                )

                query = (await session.execute(query)).scalars().all()
                return query
            except Exception as e:
                logger.error("An error has occured {}".format(e))
                raise

    async def update_by_id(
        self, id: UUID, updated_fields: UserUpdateSchema
    ) -> Union[User, None]:
        """
        Update a user by ID.

        Args:
            id (UUID): The user's unique identifier.
            updated_fields (UserUpdateSchema): Fields to update.

        Returns:
            User | None: The updated user object, or None if not found.
        """
        try:
            async with self.db_adapter.session() as session, session.begin():
                from app.models.next_of_kin import NextOfKin

                updated_fields_ = updated_fields.model_dump(
                    exclude_none=True, exclude=["next_of_kin"]
                )

                query = (
                    update(self.model)
                    .where(self.model.id == id)
                    .values({**updated_fields_})
                    .execution_options(synchronize_session="fetch")
                )

                result = await session.execute(query)

                if updated_fields.next_of_kin is not None:
                    # Then, update or insert next_of_kin separately
                    next_of_kin_data = {
                        **updated_fields.model_dump(include=["next_of_kin"]).get(
                            "next_of_kin"
                        )
                    }
                    existing_nok = (
                        await session.execute(
                            select(NextOfKin).where(NextOfKin.user_id == id)
                        )
                    ).scalar_one_or_none()

                    if existing_nok:
                        for key, value in next_of_kin_data.items():
                            setattr(existing_nok, key, value)
                    else:
                        new_nok = NextOfKin(
                            user_id=id,
                            name=next_of_kin_data.get("name"),
                            relationship=next_of_kin_data.get("relationship"),
                            phone=next_of_kin_data.get("phone"),
                            email=next_of_kin_data.get("email", None),
                        )
                        session.add(new_nok)

                updated_record = (
                    await session.execute(
                        select(self.model)
                        .where(self.model.id == id)
                        .options(
                            selectinload(self.model.role).selectinload(
                                Role.permissions
                            ),
                            selectinload(self.model.next_of_kin),
                            selectinload(self.model.permissions),
                            selectinload(self.model.bank),
                            selectinload(self.model.attendance),
                            selectinload(self.model.department),
                            selectinload(self.model.leave_requests),
                            selectinload(self.model.employment_type),
                            selectinload(self.model.payroll_class),
                            selectinload(self.model.pension),
                        )
                    )
                ).scalar_one_or_none()

                if result.rowcount < 1:
                    return updated_record

                return updated_record
        except Exception as e:
            await self.db_adapter.rollback(session)
            raise

    async def attach_role(self, user_id: UUID, role_id: UUID) -> None:
        """Add user role"""
        async with self.session_scope() as session:
            try:
                link = UserRoleLink(user_id=user_id, role_id=role_id)
                session.add(link)
                await session.flush()
            except IntegrityError as e:
                logger.error("Integrity error attaching role: %s", e)
                raise
            except Exception as e:
                logger.error("Unexpected error attaching role: %s", e)
                raise

    async def attach_permission(self, user_id: UUID, permission_id: UUID) -> None:
        """Add user permissions"""
        async with self.session_scope() as session:
            try:
                link = UserPermissionLink(user_id=user_id, permission_id=permission_id)
                session.add(link)
                await session.flush()
            except IntegrityError as e:
                logger.error("Integrity error attaching permission: %s", e)
                raise
            except Exception as e:
                logger.error("Unexpected error attaching permission: %s", e)
                raise
