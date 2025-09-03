"""
Custom integration to integrate panda_status with Home Assistant.

For more details about this integration, please refer to
https://github.com/ping-localhost/panda_status
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.const import CONF_URL, Platform

from .const import DOMAIN, LOGGER
from .coordinator import PandaStatusDataUpdateCoordinator
from .data import PandaStatusData
from .websocket import PandaStatusWebSocket

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import PandaStatusConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.SELECT,
    Platform.SWITCH,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: PandaStatusConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = PandaStatusDataUpdateCoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
    )
    entry.runtime_data = PandaStatusData(
        client=PandaStatusWebSocket(url=entry.data[CONF_URL], session=None),
        coordinator=coordinator,
    )

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: PandaStatusConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: PandaStatusConfigEntry,
) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
