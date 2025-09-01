"""Switch platform for panda_status."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.switch import (
    SwitchDeviceClass,
    SwitchEntity,
    SwitchEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import callback

from custom_components.panda_status import tools

from .entity import PandaStatusEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import PandaStatusDataUpdateCoordinator
    from .data import PandaStatusConfigEntry

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: PandaStatusConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the panda_status switch platform."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        [
            PandaStatusAPSwitch(
                coordinator=coordinator,
                entity_description=SwitchEntityDescription(
                    key="ap",
                    name="AP Enabled",
                    icon="mdi:toggle-switch",
                    entity_category=EntityCategory.CONFIG,
                    device_class=SwitchDeviceClass.SWITCH,
                ),
            ),
            PandaStatusRGBIdleSwitch(
                coordinator=coordinator,
                entity_description=SwitchEntityDescription(
                    key="rgb_idle_light",
                    name="RGB Idle Light",
                    icon="mdi:lightbulb",
                    entity_category=EntityCategory.CONFIG,
                    device_class=SwitchDeviceClass.SWITCH,
                ),
            ),
        ]
    )


class PandaStatusAPSwitch(PandaStatusEntity, SwitchEntity):
    """Representation of the AP Switch."""

    def __init__(
        self,
        coordinator: PandaStatusDataUpdateCoordinator,
        entity_description: SwitchEntityDescription,
    ) -> None:
        """
        Initialize the AP Switch entity.

        Args:
            coordinator: The data update coordinator for panda_status.
            entity_description: Description of the switch entity.

        """
        super().__init__(coordinator, entity_description)
        self.entity_description = entity_description
        self._attr_is_on = self._get_state_from_data()

    def _get_state_from_data(self) -> bool | None:
        """Get the current state from coordinator data."""
        last_msg = tools.extract_value(self.coordinator.data, "ap.on")
        if last_msg is not None:
            return last_msg == 1
        return None

    async def async_turn_on(self, **kwargs: Any) -> None:  # noqa: ARG002
        """Turn on the AP."""
        await self.coordinator.config_entry.runtime_data.client.async_send(
            '{"ap":{"on":1}}'
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:  # noqa: ARG002
        """Turn off the AP."""
        await self.coordinator.config_entry.runtime_data.client.async_send(
            '{"ap":{"on":0}}'
        )
        await self.coordinator.async_request_refresh()


class PandaStatusRGBIdleSwitch(PandaStatusEntity, SwitchEntity):
    """Representation of the RGB Idle Light Switch."""

    def __init__(
        self,
        coordinator: PandaStatusDataUpdateCoordinator,
        entity_description: SwitchEntityDescription,
    ) -> None:
        """
        Initialize the RGB Idle Light Switch entity.

        Args:
            coordinator: The data update coordinator for panda_status.
            entity_description: Description of the switch entity.

        """
        super().__init__(coordinator, entity_description)
        self.entity_description = entity_description
        self._attr_is_on = self._get_state_from_data()

    def _get_state_from_data(self) -> bool | None:
        """Get the current state from coordinator data."""
        last_msg = self.coordinator.data
        if last_msg and "settings" in last_msg:
            list2 = last_msg["settings"].get("list2", [])
            if len(list2) > 1:
                return list2[1].get("brightness", 0) > 0
            return False
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_is_on = self._get_state_from_data()
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:  # noqa: ARG002
        """Turn on the RGB Idle Light."""
        await self.coordinator.config_entry.runtime_data.client.async_send(
            '{"settings":{"rgb_info_brightness":"100"}}'
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:  # noqa: ARG002
        """Turn off the RGB Idle Light."""
        await self.coordinator.config_entry.runtime_data.client.async_send(
            '{"settings":{"rgb_info_brightness":"0"}}'
        )
        await self.coordinator.async_request_refresh()
