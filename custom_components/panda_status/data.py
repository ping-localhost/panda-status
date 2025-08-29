"""Custom types for panda_status."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .coordinator import PandaStatusDataUpdateCoordinator
    from .websocket import PandaStatusWebSocket


type PandaStatusConfigEntry = ConfigEntry[PandaStatusData]


@dataclass
class PandaStatusData:
    """Data for the PandaStatus integration."""

    client: PandaStatusWebSocket
    coordinator: PandaStatusDataUpdateCoordinator
    integration: Integration
