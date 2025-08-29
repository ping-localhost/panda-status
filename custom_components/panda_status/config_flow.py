"""Adds config flow for PandaStatus."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_URL
from homeassistant.helpers import selector
from slugify import slugify

from .const import DOMAIN, LOGGER
from .websocket import (
    PandaStatusWebSocket,
    PandaStatusWebsocketCommunicationError,
    PandaStatusWebsocketError,
)


class PandaStatusFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for PandaStatus."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_credentials(
                    url=user_input[CONF_URL],
                )
            except PandaStatusWebsocketCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except PandaStatusWebsocketError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(unique_id=slugify(user_input[CONF_URL]))
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input[CONF_URL], data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_URL,
                        default=(user_input or {}).get(CONF_URL, vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                },
            ),
            errors=_errors,
        )

    async def _test_credentials(self, url: str) -> None:
        """Validate credentials."""
        client = PandaStatusWebSocket(url=url, session=None)
        await client.async_get_data()
