"""Tools for panda_status integration."""

from typing import Any


def extract_value(data: dict, dotted_key: str) -> Any:
    """Extract nested JSON value using dotted path."""
    for part in dotted_key.split("."):
        try:
            data = data[part]
        except (TypeError, KeyError):
            return None

    return data
