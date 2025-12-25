"""Tools for panda_status integration."""

from typing import Any
from urllib.parse import urlparse

import voluptuous as vol

from custom_components.panda_status import PandaStatusWebSocket, const


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


def validate_url(value: str | None) -> str:
    """Validate a WebSocket URL."""
    if value is None:
        raise vol.Invalid(const.INVALID_URL_FORMAT)

    value = vol.Coerce(str)(value)
    parsed = urlparse(value)

    if parsed.scheme not in ("ws", "wss"):
        raise vol.Invalid(const.INVALID_URL_FORMAT)

    if not parsed.netloc:
        raise vol.Invalid(const.INVALID_URL_FORMAT)

    if parsed.path.rstrip("/") != "/ws":
        raise vol.Invalid(const.INVALID_URL_FORMAT)

    return value


async def test_credentials(url: str) -> dict:
    """Validate credentials."""
    client = PandaStatusWebSocket(url=url, session=None)
    return await client.async_get_data()
