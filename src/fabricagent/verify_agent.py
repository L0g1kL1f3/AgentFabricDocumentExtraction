"""Validation helpers for extracted document metadata."""

from __future__ import annotations

from typing import Any


def find_empty_fields(data: Any, path: str = "") -> list[str]:
    """Return paths whose values are None, blank strings, empty lists, or empty dictionaries."""
    empty_fields: list[str] = []

    if isinstance(data, dict):
        if not data and path:
            return [path]
        for key, value in data.items():
            child_path = f"{path}.{key}" if path else str(key)
            empty_fields.extend(find_empty_fields(value, child_path))
        return empty_fields

    if isinstance(data, list):
        if not data and path:
            return [path]
        for index, item in enumerate(data):
            empty_fields.extend(find_empty_fields(item, f"{path}[{index}]"))
        return empty_fields

    if data is None or (isinstance(data, str) and not data.strip()):
        empty_fields.append(path)

    return empty_fields
