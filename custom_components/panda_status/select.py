"""Select platform for Panda Status integration."""

from __future__ import annotations

from enum import Enum
import logging
from typing import TYPE_CHECKING

from custom_components.panda_status import tools
from custom_components.panda_status.coordinator import PandaStatusDataUpdateCoordinator
from custom_components.panda_status.data import PandaStatusConfigEntry
from custom_components.panda_status.entity import PandaStatusEntity
from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import callback

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import PandaStatusDataUpdateCoordinator
    from .data import PandaStatusConfigEntry

_LOGGER = logging.getLogger(__name__)


class LightEffectMode(Enum):
    """
    An enumeration representing different light effect modes.

    Members:
        MUSIC (int): Light effect mode for music, value 0.
        H2D (int): Light effect mode for H2D, value 1.
    """

    MUSIC = 0
    H2D = 1

    @classmethod
    def from_value(cls, value: int) -> LightEffectMode:
        """Return the LightEffectMode corresponding to the given integer value."""
        for mode in cls:
            if mode.value == value:
                return mode

        _LOGGER.warning(
            "Value %d does not match any LightEffectMode, defaulting to MUSIC", value
        )
        return cls.MUSIC

    @classmethod
    def display_names(cls) -> dict[LightEffectMode, str]:
        """Return a mapping of LightEffectMode to display names."""
        return {
            cls.MUSIC: "Music",
            cls.H2D: "H2D",
        }

    @property
    def display_name(self) -> str:
        """Return the display name for this LightEffectMode."""
        return self.display_names().get(self, self.name)

    @classmethod
    def from_display_name(cls, value: str) -> LightEffectMode:
        """Return the LightEffectMode corresponding to a display name."""
        for mode, display_name in cls.display_names().items():
            if display_name.lower() == value.lower():
                return mode

        _LOGGER.warning(
            "Display name %s does not match any LightEffectMode, defaulting to MUSIC",
            value,
        )
        return cls.MUSIC

    @classmethod
    def names(cls) -> list[str]:
        """Return a list of display names for each LightEffectMode."""
        return [mode.display_name for mode in cls]


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: PandaStatusConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the panda_status select platform."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        [
            LightEffectSelect(
                coordinator=coordinator,
                entity_description=SelectEntityDescription(
                    key="light_effect_mode",
                    name="Light Effect Mode",
                    icon="mdi:lightning-bolt",
                    entity_category=EntityCategory.CONFIG,
                ),
            ),
        ]
    )


class LightEffectSelect(PandaStatusEntity, SelectEntity):
    """Select to choose Light Effect mode."""

    def __init__(
        self,
        coordinator: PandaStatusDataUpdateCoordinator,
        entity_description: SelectEntityDescription,
    ) -> None:
        """
        Initialize the Light Effect Select entity.

        Args:
            coordinator: The data update coordinator for panda_status.
            entity_description: Description of the select entity.

        """
        super().__init__(coordinator, entity_description)
        self.entity_description = entity_description
        self._current_mode = self._get_state_from_data()

    @property
    def options(self) -> list[str]:
        """Returns a list of available light effect mode names."""
        return LightEffectMode.names()

    @property
    def current_option(self) -> str:
        """Return the currently selected light effect mode."""
        return self._current_mode.display_name

    async def async_select_option(self, option: str) -> None:
        """Change the selected light effect mode."""
        mode = LightEffectMode.from_display_name(option)
        await self.coordinator.config_entry.runtime_data.client.async_send(
            '{"settings":{"rgb_info_mode":' + str(mode.value) + "}}"
        )
        self._current_mode = mode
        self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        self._current_mode = self._get_state_from_data()
        self.async_write_ha_state()

    def _get_state_from_data(self) -> LightEffectMode:
        """Get the current state from coordinator data."""
        mode = tools.extract_value(self.coordinator.data, "settings.current_mode")
        if mode is not None:
            return LightEffectMode.from_value(mode)

        return LightEffectMode.MUSIC
