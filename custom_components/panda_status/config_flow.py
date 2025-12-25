"""Adds config flow for PandaStatus."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from custom_components.panda_status import const, tools
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_NAME, CONF_URL
from homeassistant.helpers import selector

from .const import DOMAIN, LOGGER
from .websocket import PandaStatusWebsocketCommunicationError, PandaStatusWebsocketError


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
                url = tools.validate_url(user_input.get(CONF_URL))
            except vol.Invalid:
                errors[CONF_URL] = const.INVALID_URL_FORMAT
            else:
                try:
                    initial_data = await tools.test_credentials(url=url)
                except PandaStatusWebsocketCommunicationError as exception:
                    LOGGER.error(exception)
                    errors["base"] = "connection"
                except PandaStatusWebsocketError as exception:
                    LOGGER.exception(exception)
                    errors["base"] = "unknown"
                else:
                    await self._async_handle_discovery_without_unique_id()

                    printer_name = tools.get_printer_name(initial_data=initial_data)
                    device_name = user_input.get(CONF_NAME) or tools.get_device_name(
                        initial_data=initial_data
                    )

                    return self.async_create_entry(
                        title=device_name,
                        description=f"Panda status for {printer_name}",
                        data={
                            CONF_URL: url,
                            CONF_NAME: device_name,
                        },
                    )

        # Ensure default value for URL is provided
        suggested_values = {
            CONF_URL: "ws://192.168.0.33/ws",
        }
        if user_input:
            suggested_values.update(user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_URL): selector.TextSelector(
                            selector.TextSelectorConfig(
                                type=selector.TextSelectorType.URL
                            ),
                        ),
                        vol.Optional(CONF_NAME): selector.TextSelector(
                            selector.TextSelectorConfig(
                                type=selector.TextSelectorType.TEXT
                            )
                        ),
                    }
                ),
                suggested_values=suggested_values,
            ),
            errors=errors,
            last_step=True,
        )
