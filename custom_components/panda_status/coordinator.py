"""DataUpdateCoordinator for panda_status."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .websocket import PandaStatusWebsocketCommunicationError, PandaStatusWebsocketError

if TYPE_CHECKING:
    from .data import PandaStatusConfigEntry


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class PandaStatusDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: PandaStatusConfigEntry

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            return await self.config_entry.runtime_data.client.async_get_data()
        except PandaStatusWebsocketCommunicationError as exception:
            raise ConfigEntryNotReady(exception) from exception
        except PandaStatusWebsocketError as exception:
            raise UpdateFailed(exception) from exception
