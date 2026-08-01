"""DataUpdateCoordinator for panda_status."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .websocket import (
    PandaStatusWebsocketCommunicationError,
    PandaStatusWebsocketError,
    PandaStatusWebsocketTimeoutError,
)

if TYPE_CHECKING:
    from .data import PandaStatusConfigEntry


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class PandaStatusDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: PandaStatusConfigEntry

    async def _async_update_data(self) -> Any:
        """Update data via library.

        A single slow/timed-out poll is retried once before being treated
        as a real failure. With periodic polling now running continuously
        rather than only right after user actions, occasionally catching
        the device's embedded WS stack mid-task is expected background
        noise, not a genuine unavailability - retrying once avoids flapping
        entities to unavailable over what is usually just a slow beat.
        """
        attempts = 2
        for attempt in range(attempts):
            try:
                return await self.config_entry.runtime_data.client.async_get_data()
            except PandaStatusWebsocketTimeoutError as exception:
                if attempt == attempts - 1:
                    raise UpdateFailed(exception) from exception
            except PandaStatusWebsocketCommunicationError as exception:
                raise ConfigEntryNotReady(exception) from exception
            except PandaStatusWebsocketError as exception:
                raise UpdateFailed(exception) from exception
        return None  # pragma: no cover - unreachable, loop always returns or raises
