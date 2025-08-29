"""WebSocket Client."""

from __future__ import annotations

import json
import logging

import async_timeout
from websockets.asyncio.client import ClientConnection, connect
from websockets.exceptions import ConnectionClosed

_LOGGER = logging.getLogger(__name__)


class PandaStatusWebsocketError(Exception):
    """Exception to indicate a general WebSocket error."""


class PandaStatusWebsocketCommunicationError(
    PandaStatusWebsocketError,
):
    """Exception to indicate a communication error."""


class PandaStatusWebSocket:
    """WebSocket Client for Panda Status."""

    _url: str
    _session: ClientConnection

    def __init__(self, url: str, session: ClientConnection | None) -> None:
        """
        Initialize the WebSocket client.

        Args:
            url: The WebSocket URL.
            session: An optional existing ClientConnection.

        """
        self._url = url

        if session is None:
            self._session = connect(self._url)  # pyright: ignore[reportAttributeAccessIssue]
        else:
            self._session = session

    async def async_get_data(self) -> dict:
        """
        Fetch data from the WebSocket.

        Returns:
            Parsed JSON data from the WebSocket.

        Raises:
            PandaStatusWebsocketError: If JSON is invalid or connection fails.

        """
        async with self._session as websocket:
            try:
                data = json.loads(await websocket.recv())
            except TimeoutError as e:
                msg = f"Timeout error getting data - {e}"
                raise PandaStatusWebsocketCommunicationError(msg) from e
            except (OSError, ConnectionClosed, TypeError) as e:
                msg = f"Communication error - {e}"
                raise PandaStatusWebsocketCommunicationError(msg) from e
            except Exception as e:
                msg = f"Unexpected error parsing data payload - {e}"
                raise PandaStatusWebsocketError(msg) from e

        _LOGGER.debug("Latest data received: %s", json.dumps(data))

        return data

    async def async_send(self, payload: str) -> None:
        """
        Send a payload to the WebSocket.

        Args:
            payload: The string payload to send.

        Raises:
            PandaStatusWebsocketCommunicationError: On communication errors.
            PandaStatusWebsocketError: On unexpected errors.

        """
        try:
            _LOGGER.debug("Sending payload: %s", payload)
            async with async_timeout.timeout(1) and self._session as websocket:
                await websocket.send(payload)
                _LOGGER.debug("Payload sent: %s", payload)
        except TimeoutError as e:
            msg = f"Timeout error sending payload - {e}"
            raise PandaStatusWebsocketCommunicationError(msg) from e
        except (OSError, ConnectionClosed, TypeError) as e:
            msg = f"Communication error - {e}"
            raise PandaStatusWebsocketCommunicationError(msg) from e
        except Exception as e:
            msg = f"Unexpected error sending payload - {e}"
            raise PandaStatusWebsocketError(msg) from e
