#!/usr/bin/env python3
# File: app/adapter/json_adapter.py
# Author: Oluwatobiloba Light
"""JSON File Database Adapter"""

import json
import os
from typing import Any, List, Dict
from app.adapter.database_adapter import DatabaseAdapter
from app.core.exceptions import DuplicatedError
from app.schemas.user_schema import UserSchema


class JSONAdapter(DatabaseAdapter):
    def __init__(self, file_path: str = "db.json") -> None:
        self.file_path = file_path

        if not os.path.exists(self.file_path):
            self._save_data({})

    def _load_data(self) -> Dict[str, Any]:
        with open(self.file_path, "r") as file:
            return json.load(file)

    def _save_data(self, data: Dict[str, Any]) -> None:
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    def add(self, table: str, instance: Dict[str, any]):
        """Add a new record"""
        data = self._load_data()

        if table not in data:
            data[table] = {}  # Create the table if it doesn't exist

        staff_id = str(instance["staff_id"])
        email = instance["email"]

        if staff_id in data[table]:
            raise DuplicatedError(detail="Staff ID is a duplicate!")

        # Check for duplicate email (across all entries in the table)
        for existing_staff_id, existing_instance in data[table].items():
            # use .get to avoid KeyError
            if existing_instance.get("email") == email:
                raise DuplicatedError(detail="Email is a duplicate!")

        data[table][staff_id] = instance  # Add the new instance
        self._save_data(data)
        return {table: {staff_id: instance}}

    async def flush(self) -> None:
        """Flush is not needed for file-based storage"""
        pass

    async def refresh(self, instance: Any) -> None:
        """Refresh is not applicable for file-based storage"""
        pass

    async def commit(self) -> None:
        """Commit is not needed as data is saved immediately"""
        pass

    async def rollback(self) -> None:
        """Rollback is not applicable for file-based storage"""
        pass

    async def get_by_id(self, table: str, id: str):
        """Retrieve a user"""
        data = self._load_data()

        if table in data:
            if id in data[table]:
                return data[table][id]
            return None
        else:
            return None

    async def delete(self, instance: Dict) -> None:
        """Delete a record"""
        data = self._load_data()
        filtered_data = [record for record in data if record.get(
            "id") !=
            instance.get("id")]
        self._save_data(filtered_data)
