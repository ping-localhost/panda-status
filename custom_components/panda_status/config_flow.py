"""Adds config flow for PandaStatus."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from custom_components.panda_status import tools
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_NAME, CONF_URL
from homeassistant.helpers import selector

from .const import DOMAIN, LOGGER
from .websocket import PandaStatusWebsocketCommunicationError, PandaStatusWebsocketError

OPTIONS_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_URL): selector.TextSelector(
            selector.TextSelectorConfig(type=selector.TextSelectorType.TEXT)
        ),
        vol.Optional(CONF_NAME): selector.TextSelector(
            selector.TextSelectorConfig(type=selector.TextSelectorType.TEXT)
        ),
    }
)


class PandaStatusFlowHandler(ConfigFlow, domain=DOMAIN):
    """Config flow for PandaStatus."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initialized by the user."""
        errors = {}
        if user_input is not None:
            try:
                # Try and get initial data to validate the connection
                initial_data = await tools.test_credentials(
                    url=user_input.get(CONF_URL)
                )
            except PandaStatusWebsocketCommunicationError as exception:
                LOGGER.error(exception)
                errors["base"] = "connection"
            except PandaStatusWebsocketError as exception:
                LOGGER.exception(exception)
                errors["base"] = "unknown"
            else:
                # Check if a config entry already exists
                await self._async_handle_discovery_without_unique_id()

                # Use tools to extract printer and device name
                printer_name = tools.get_printer_name(initial_data=initial_data)
                device_name = user_input.get(CONF_NAME, None) or tools.get_device_name(
                    initial_data=initial_data
                )

                # If user provided a name, use it; otherwise, use the device name
                return self.async_create_entry(
                    title=device_name,
                    description=f"Panda status for {printer_name}",
                    data={
                        CONF_URL: user_input.get(CONF_URL),
                        CONF_NAME: device_name,
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=OPTIONS_SCHEMA,
            errors=errors,
        )
