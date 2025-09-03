"""System Health platform for panda_status custom component."""

from typing import TYPE_CHECKING, Any

from custom_components.panda_status.const import DOMAIN
from homeassistant.components import system_health
from homeassistant.const import CONF_URL
from homeassistant.core import HomeAssistant, callback

if TYPE_CHECKING:
    from .data import PandaStatusConfigEntry


@callback
def async_register(
    hass: HomeAssistant,  # noqa: ARG001
    register: system_health.SystemHealthRegistration,
) -> None:
    """Register system health callbacks."""
    register.async_register_info(system_health_info)


async def system_health_info(hass: HomeAssistant) -> dict[str, Any]:
    """Get info for the info page."""
    config_entry: PandaStatusConfigEntry = hass.config_entries.async_entries(DOMAIN)[0]

    return {
        "can_reach_server": system_health.async_check_can_reach_url(
            hass, config_entry.data[CONF_URL]
        ),
    }
