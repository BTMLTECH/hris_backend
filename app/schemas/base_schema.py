#!/usr/bin/env python3
# File: app/schemas/base_schema.py
# Author: Oluwatobiloba Light
"""Base Schema"""


from datetime import datetime
from typing import Optional, Union
from uuid import UUID
from pydantic import BaseModel


class ModelBaseInfo(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime

    # class Config:
    #     model_config = ConfigDict(
    #         arbitrary_types_allowed=True, from_attributes=True)
    #     from_attributes = True
    #     orm_mode = True


class FindBase(BaseModel):
    ordering: Optional[str]
    page: Optional[int]
    page_size: Optional[Union[int, str]]
    pages: Optional[int]
