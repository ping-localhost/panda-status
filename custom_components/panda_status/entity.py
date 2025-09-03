"""PandaStatusEntity class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.panda_status import tools
from homeassistant.const import CONF_NAME
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import PandaStatusDataUpdateCoordinator

if TYPE_CHECKING:
    from homeassistant.helpers.entity import EntityDescription


class PandaStatusEntity(CoordinatorEntity[PandaStatusDataUpdateCoordinator]):
    """PandaStatusEntity class."""

    def __init__(
        self,
        coordinator: PandaStatusDataUpdateCoordinator,
        entity_description: EntityDescription,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)

        self._attr_device_info = DeviceInfo(
            manufacturer="BigTreeTech",
            model="Panda Status",
            sw_version=tools.extract_value(coordinator.data, "settings.fw_version"),
            name=coordinator.config_entry.data[CONF_NAME],
            identifiers={
                (
                    coordinator.config_entry.domain,
                    coordinator.config_entry.entry_id,
                )
            },
        )

        self._attr_unique_id = (
            f"{DOMAIN}_{coordinator.config_entry.unique_id}_{entity_description.key}"
        )
