"""Adds config flow for PandaStatus."""

from __future__ import annotations

import voluptuous as vol

from custom_components.panda_status import tools
from homeassistant import config_entries
from homeassistant.config_entries import OptionsFlowWithReload
from homeassistant.const import CONF_NAME, CONF_URL
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import DOMAIN, LOGGER
from .websocket import (
    PandaStatusWebSocket,
    PandaStatusWebsocketCommunicationError,
    PandaStatusWebsocketError,
)

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


async def _test_credentials(url: str) -> dict:
    """Validate credentials."""
    client = PandaStatusWebSocket(url=url, session=None)
    return await client.async_get_data()


class PandaStatusFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for PandaStatus."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(
        self, user_input: dict | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        errors = {}
        if user_input is not None:
            try:
                # Try and get initial data to validate the connection
                initial_data = await _test_credentials(url=user_input[CONF_URL])
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
                device_name = user_input[CONF_NAME] or tools.get_device_name(
                    initial_data=initial_data
                )

                # If user provided a name, use it; otherwise, use the device name
                return self.async_create_entry(
                    title=device_name,
                    description=f"Panda status for {printer_name}",
                    data={
                        CONF_URL: user_input[CONF_URL],
                        CONF_NAME: device_name,
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=OPTIONS_SCHEMA,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Return the options flow handler for PandaStatus."""
        return PandaStatusOptionsFlowHandler(config_entry)


class PandaStatusOptionsFlowHandler(OptionsFlowWithReload):
    """Options flow for PandaStatus."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict | None = None
    ) -> config_entries.ConfigFlowResult:
        """Manage the options."""
        errors = {}
        if user_input is not None:
            try:
                # Try and get initial data to validate the connection
                initial_data = await _test_credentials(url=user_input[CONF_URL])
            except PandaStatusWebsocketCommunicationError as exception:
                LOGGER.error(exception)
                errors["base"] = "connection"
            except PandaStatusWebsocketError as exception:
                LOGGER.exception(exception)
                errors["base"] = "unknown"
            else:
                # Use tools to extract printer and device name
                printer_name = tools.get_printer_name(initial_data=initial_data)
                device_name = user_input[CONF_NAME] or tools.get_device_name(
                    initial_data=initial_data
                )

                # If user provided a name, use it; otherwise, use the device name
                return self.async_create_entry(
                    title=device_name,
                    description=f"Panda status for {printer_name}",
                    data={
                        CONF_URL: user_input[CONF_URL],
                        CONF_NAME: device_name,
                    },
                )

        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                OPTIONS_SCHEMA, self.config_entry.options
            ),
            errors=errors,
        )
