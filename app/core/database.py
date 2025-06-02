#!/usr/bin/env python3
# File: app/core/database.py
# Author: Oluwatobiloba Light
"""HRIS Database"""

from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator
from redis.asyncio.client import Redis
import redis.asyncio as redis
from sqlalchemy.orm import DeclarativeBase, declarative_base
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from app.core.config import hris_config


Base: DeclarativeBase = declarative_base()


class Database:
    """"""

    def __init__(self, db_url: str) -> None:
        self._engine: AsyncEngine = create_async_engine(
            db_url,
            pool_pre_ping=True,
            echo=False,
            # connect_args={"ssl": True if hris_config.ENV ==
            #               "production" else False},
        )

        self._sessionmaker = async_sessionmaker(
            self._engine,
            expire_on_commit=False,
            autoflush=False,
            future=True,
            class_=AsyncSession,
        )

    async def close(self):
        if self._engine is None:
            raise Exception("Database SessionManager is not initialized")
        await self._engine.dispose()

    async def create_async_database(self) -> None:
        if self._engine:
            async with self._engine.connect() as conn:
                if hris_config.ENV == "development" or hris_config.ENV == "dev":
                    # Drop dependent tables explicitly
                    await conn.run_sync(Base.metadata.drop_all, checkfirst=True)

                # await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all, checkfirst=True)

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, Any]:
        if self._sessionmaker is None:
            raise Exception("Database SessionManager is not initialized")

        sessionmanager: AsyncSession = self._sessionmaker()

        async with sessionmanager as conn:
            try:
                yield conn
                await conn.commit()
            except Exception as e:
                await conn.rollback()
                raise e
            finally:
                await conn.close()


class RedisConnection:
    """Redis Cache"""

    def __init__(
        self,
        host: str = (
            "redis://localhost" if hris_config.ENV == "dev" else hris_config.REDIS_URL
        ),
        port: int = 6379,
        db: int = 0,
    ):
        # self.pool = redis.ConnectionPool(
        #     host=host, port=port, db=db, max_connections=20)
        self.pool = redis.ConnectionPool().from_url(host)
        self._client = redis.Redis.from_pool(connection_pool=self.pool)

    async def close(self) -> None:
        """Close the connection pool."""
        """Close the Redis connection pool."""
        if self._client is None:
            raise Exception("Redis connection pool is not initialized.")
        await self._client.connection.disconnect()

    @asynccontextmanager
    async def connection(self) -> AsyncGenerator[Redis, Any]:
        """
        Provide an async Redis client for usage.

        Example:
        async with redis_client.connection() as redis:
            await redis.set("key", "value")
        """
        if self._client is None:
            raise Exception("Redis client is not initialized.")
        try:
            yield self._client
        except Exception as e:
            raise e
