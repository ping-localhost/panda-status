"""System health platform for the Panda Status custom component."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, cast

from homeassistant.const import CONF_URL
from homeassistant.core import HomeAssistant, callback

from . import tools
from .const import DOMAIN
from .websocket import PandaStatusWebsocketError, PandaStatusWebsocketTimeoutError

if TYPE_CHECKING:
    from homeassistant.components import system_health

    from .data import PandaStatusConfigEntry

_LOGGER = logging.getLogger(__name__)


@callback
def async_register(
    hass: HomeAssistant,  # noqa: ARG001
    register: system_health.SystemHealthRegistration,
) -> None:
    """Register system health callbacks."""
    register.async_register_info(system_health_info)


async def system_health_info(hass: HomeAssistant) -> dict[str, Any]:
    """Return system-health information for the Panda Status integration."""
    # Grab the first config entry for this integration.
    # If none are present we report nothing.
    config_entries = hass.config_entries.async_entries(DOMAIN)
    if not config_entries:
        _LOGGER.warning("No %s config entries found", DOMAIN)
        return {}

    config_entry: PandaStatusConfigEntry = cast(
        "PandaStatusConfigEntry", config_entries[0]
    )

    url = config_entry.data.get(CONF_URL)
    if not url:
        _LOGGER.warning("Config entry for %s does not contain a URL", DOMAIN)
        return {"websocket_reachable": "Missing URL"}

    try:
        await tools.test_credentials(url)
    except (TimeoutError, PandaStatusWebsocketTimeoutError):
        data = "timeout"
    except (Exception, PandaStatusWebsocketError):  # noqa: BLE001
        data = "unreachable"
    else:
        data = "ok"

    return {"websocket_reachable": data}
