"""Sensor platform for panda_status."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.const import EntityCategory

from custom_components.panda_status import tools

from .entity import PandaStatusEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import PandaStatusDataUpdateCoordinator
    from .data import PandaStatusConfigEntry

_LOGGER = logging.getLogger(__name__)


ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="ap.ssid",
        name="AP SSID",
        icon="mdi:wifi",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="sta.ip",
        name="Device IP",
        icon="mdi:ip-network",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="sta.hostname",
        name="Hostname",
        icon="mdi:server-network",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="sta.state",
        name="WiFi State",
        icon="mdi:information-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="printer.name",
        name="Printer Name",
        icon="mdi:printer",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="printer.ip",
        name="Printer IP",
        icon="mdi:ip-network-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="printer.state",
        name="Printer State",
        icon="mdi:printer-alert",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="settings.fw_version",
        name="Firmware Version",
        icon="mdi:chip",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: PandaStatusConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = entry.runtime_data.coordinator
    entities = [
        PandaStatusSensor(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    ]
    async_add_entities(entities)


class PandaStatusSensor(PandaStatusEntity, SensorEntity):
    """Representation of a Panda Status sensor."""

    def __init__(
        self,
        coordinator: PandaStatusDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize a PandaStatusSensor with coordinator and entity description."""
        super().__init__(coordinator, entity_description)
        self.entity_description = entity_description

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        return tools.extract_value(self.coordinator.data, self.entity_description.key)
