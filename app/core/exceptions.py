#!/usr/bin/env python3
# File: app/core/exceptions.py
# Author: Oluwatobiloba Light
"""Exceptions"""


from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class DuplicatedError(HTTPException):
    def __init__(
        self, detail: Any = None, headers: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, detail, headers)

    def __str__(self) -> str:
        # Only return the detail without the status code
        return str(self.detail)


class CustomDatabaseError(Exception):
    """Custom exception for database-raised errors."""

    def __init__(self, message: str, original_exception: Exception = None):
        super().__init__(message)
        self.original_exception = original_exception

    def __str__(self):
        if self.original_exception:
            return f"{self.args[0]}"
        return self.args[0]


class UnauthorizedError(HTTPException):
    def __init__(
        self, detail: Any = None, headers: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, headers)

    def __str__(self) -> str:
        # Only return the detail without the status code
        return str(self.detail)


class AuthForbiddenError(HTTPException):
    def __init__(
        self, detail: Any = None, headers: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, detail, headers)

    def __str__(self) -> str:
        # Only return the detail without the status code
        return str(self.detail)
        


class NotFoundError(HTTPException):
    def __init__(
        self, detail: Any = None, headers: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, detail, headers)

    def __str__(self) -> str:
        # Only return the detail without the status code
        return str(self.detail)


class ValidationError(HTTPException):
    def __init__(
        self, detail: Any = None, headers: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, detail, headers)

    def __str__(self) -> str:
        # Only return the detail without the status code
        return str(self.detail)


class ServerError(HTTPException):
    def __init__(
        self, detail: Any = None, headers: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, detail, headers)

    def __str__(self) -> str:
        # Only return the detail without the status code
        return str(self.detail)


class GeneralError(HTTPException):
    def __init__(
        self,
        detail: Any = None,
        status_code: Optional[int] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            status_code=status_code if status_code else status.HTTP_400_BAD_REQUEST,
            detail=detail,
            headers=headers,
        )

    def __str__(self) -> str:
        # Only return the detail without the status code
        return str(self.detail)
