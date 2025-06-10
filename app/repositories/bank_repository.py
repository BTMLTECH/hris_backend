#!/usr/bin/env python3
# File: repositories/bank_repository.py
# Author: Oluwatobiloba Light
"""Bank Repository"""

from uuid import UUID, uuid4
from sqlalchemy import delete, select, update
from app.adapter.json_adapter import JSONAdapter
from app.adapter.sqlalchemy_adapter import SQLAlchemyAdapter
from app.models.bank import Bank
from app.schemas.bank_schema import CreateBankSchema, UpdateBankSchema
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

T = TypeVar("T", bound=Bank)


class BankRepository(BaseRepository):
    def __init__(self, db_adapter: Union[JSONAdapter, SQLAlchemyAdapter]):
        self.db_adapter = db_adapter
        self.model = Bank

        super().__init__(db_adapter, Bank)

    async def create(self, schema: CreateBankSchema) -> Bank:
        """Creates a new bank record"""

        query = self.model(**schema.model_dump())

        if isinstance(self.db_adapter, SQLAlchemyAdapter):
            async with self.db_adapter.session() as session, session.begin():
                try:
                    self.db_adapter.add(session, query)
                    await self.db_adapter.flush(session)
                    await self.db_adapter.refresh(session, query)

                    query_result = (
                        select(self.model)
                        .where(self.model.id == query.id)
                        .options(selectinload(self.model.users))
                    )

                    query = (await session.execute(query_result)).scalar_one()
                except IntegrityError as e:
                    await self.db_adapter.rollback(session)
                    raise CustomDatabaseError(message=str(e), original_exception=e)
                except Exception as e:
                    if "duplicate" in str(e).lower():
                        error_msg = "Bank already exists!"
                        # raise error_msg
                        raise DuplicatedError(detail=error_msg)
                    else:
                        print(f"Other integrity error: {str(e)}")
                        raise GeneralError(detail=str(e))
                else:
                    await self.db_adapter.commit(session)
        elif isinstance(self.db_adapter, JSONAdapter):
            query.id = str(uuid4())
            self.db_adapter.add("permissions", query.model_dump(exclude_none=True))

        return query

    async def get_by_id(self, id: UUID) -> Union[Bank, None]:
        """Get a bank record from the database by ID"""
        query = (
            select(self.model)
            .where(self.model.id == id)
            .options(selectinload(self.model.users))
        )

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
            raise NotFoundError(detail="Bank does not exist or ID is invalid")

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

    async def get_all(self) -> Sequence[Bank]:
        """Gets all bank records from the database"""
        async with self.db_adapter.session() as session, session.begin():
            try:
                query = select(self.model).options(selectinload(self.model.users))

                result = (await session.execute(query)).scalars().all()

                return result
            except Exception as e:
                raise GeneralError(detail=str(e))

    async def get_by_name(self, name: str) -> Optional[Bank]:
        """Get a bank by name"""
        async with self.session_scope() as session:
            result = await session.execute(
                select(self.model).where(self.model.name.lower() == name.lower())
            )
            return result.scalars().first()

    async def update_by_id(self, id: UUID, bank_fields: UpdateBankSchema):
        try:
            async with self.session_scope() as session:
                query = (
                    update(self.model)
                    .where(self.model.id == id)
                    .values({**bank_fields.model_dump(exclude_none=True)})
                    .execution_options(synchronize_session="fetch")
                )

                result = await session.execute(query)

                updated_record = (
                    await session.execute(
                        select(self.model)
                        .where(self.model.id == id)
                        .options(selectinload(self.model.users))
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

    async def delete_by_id(self, id: UUID) -> bool:
        try:
            async with self.session_scope() as session:
                bank = (
                    await session.execute(select(self.model).where(self.model.id == id))
                ).scalar_one_or_none()

                if not bank:
                    return False

                await session.delete(bank)
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
