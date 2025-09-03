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


def get_printer_name(initial_data: dict) -> str:
    """Get printer name from initial data."""
    return extract_value(initial_data, "printer.name")


def get_device_name(initial_data: dict) -> str:
    """Get device name from initial data."""
    return f"{extract_value(initial_data, 'printer.name')} - Panda Status"
