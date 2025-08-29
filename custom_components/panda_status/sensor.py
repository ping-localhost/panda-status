"""Sensor platform for panda_status."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .entity import PandaStatusEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import PandaStatusDataUpdateCoordinator
    from .data import PandaStatusConfigEntry

_LOGGER = logging.getLogger(__name__)

SENSOR_MAP = {
    "sta.ip": "Device IP",
    "sta.hostname": "Hostname",
    "sta.state": "WiFi State",
    "printer.name": "Printer Name",
    "printer.ip": "Printer IP",
    "printer.state": "Printer State",
    "settings.fw_version": "Firmware Version",
    "settings.language": "Language",
}

ENTITY_DESCRIPTIONS = tuple(
    SensorEntityDescription(
        key=key,
        name=f"Panda {name}",
        icon="mdi:information-outline",
    )
    for key, name in SENSOR_MAP.items()
)


def _extract_value(data: dict, dotted_key: str) -> Any:
    """Extract nested JSON value using dotted path."""
    for part in dotted_key.split("."):
        data = data[part]

    return data


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
        return _extract_value(self.coordinator.data, self.entity_description.key)
