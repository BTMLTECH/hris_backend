#!/usr/bin/env python3
# File: app/main.py
# Author: Oluwatobiloba Light
"""HRIS Entry Point"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.core.config import hris_config
from app.core.container import Container
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis
from app.api.routes import routers
from app.utils.class_object import singleton


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create database connection and any other async resources
    db = app.state.db
    # redis_client = app.state.redis_client

    try:
        await db.create_async_database()
        print("✅ Database initialized")
        # redis_client.connection()
        # print("✅ Redis cache initialized")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        raise e

    yield  # FastAPI is running

    # Shutdown
    print("🛑 Shutting down...")
    await db.close()
    # await redis_client.close()


@singleton
class AppCreator:
    def __init__(self):
        # Create container first
        self.container = Container()

        # Get database from container
        self.db = self.container.db()

        # self.redis_client = self.container.redis_client()

        # set app default
        self.app = FastAPI(
            title=hris_config.PROJECT_NAME,
            # openapi_url=f"{hris_config.API}/openapi.json",
            version="0.0.1",
            description="HRIS FastAPI Web Server",
            lifespan=lifespan,
        )

        # Store db in app state for access in lifespan context manager
        self.app.state.db = self.db
        # self.app.state.redis_client = self.redis_client

        if hris_config.SECRET_KEY is None:
            raise "Missing Secret Key"

        self.app.add_middleware(
            SessionMiddleware,
            secret_key=hris_config.SECRET_KEY,
            max_age=1800,  # 30 minutes
            same_site="lax",
        )

        # set cors
        if hris_config.BACKEND_CORS_ORIGINS:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=[
                    str(origin) for origin in hris_config.BACKEND_CORS_ORIGINS
                ],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        # set routes
        @self.app.get("/")
        def root():
            return "service is working"

        @self.app.middleware("http")
        async def db_session_middleware(request: Request, call_next):
            """Middleware to manage database sessions."""
            request.state.db = AsyncSession(autocommit=False, autoflush=False)

            # pool = redis.ConnectionPool().from_url(
            #     "redis://localhost" if hris_config.ENV == "dev" else hris_config.REDIS_URL)

            # redis_conn = redis.Redis.from_pool(
            #     connection_pool=pool)

            # request.state.redis = redis_conn
            try:
                response = await call_next(request)
                # await request.state.db.commit()
                return response
            except Exception as e:
                await request.state.db.rollback()
                raise e
            finally:
                await request.state.db.close()
                # await request.state.redis.aclose()

        self.app.include_router(routers, prefix=hris_config.API)


app_creator = AppCreator()

app = app_creator.app


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc):
    errors = {}
    for error in exc.errors():
        field = "".join(error["loc"][1]) if len(error["loc"]) > 1 else error["loc"][0]
        errors["{}".format(field)] = error["msg"]
        # errors['message'] = error['msg']
        # errors.append({
        #     'field': field,
        #     'message': error['msg']
        # })
    return JSONResponse(
        status_code=422, content={"detail": "Validation error", "errors": errors}
    )


db = app_creator.db
# redis_client = app_creator.redis_client

print("✅ HRIS server Up and running...")

# print(db._engine.url)

container = app_creator.container
