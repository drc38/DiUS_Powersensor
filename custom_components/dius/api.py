"""Sample API Client."""
import asyncio
import json
import logging
import socket

from .enums import Msg_keys
from .enums import Msg_values


_LOGGER: logging.Logger = logging.getLogger(__package__)


class DiusApiClient:
    def __init__(self, host: str, port: int) -> None:
        """Sample API Client."""
        self._host = host
        self._port = port
        self._server_address = (host, port)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._open = False
        self._data = {}

    async def start(self):
        """Start socket and listen"""
        await self.run([self.open_socket(), self.listen()])

    async def listen(self):
        """Listen for incoming messages"""
        while self._open:
            message = self._socket.recv(1024)
            _LOGGER.debug("Received message %s", message)
            await self.process_message(message)

    async def open_socket(self):
        """Open connection and subscribe to data"""
        self._socket.connect(self._server_address)
        self._open = True
        while True:
            await self.subscribe()
            await asyncio.sleep(150)

    async def process_message(self, raw_msg):
        """Process json messages received"""
        msg = json.loads(raw_msg)

        type = msg.get(Msg_keys.type)
        subtype = msg.get(Msg_keys.subtype)
        device = msg.get(Msg_keys.device)

        if type == Msg_values.instant_power:
            if device == Msg_values.sensor:
                self._data[Msg_values.sensor] = msg
            if device == Msg_values.plug:
                self._data[Msg_values.plug] = msg

        if type == Msg_values.subscription and subtype == Msg_values.warning:
            _LOGGER.warning("The socket stream had a warning, resubscribing")
            await self.subscribe()

        if type == Msg_values.subscription and subtype == Msg_values.expiry:
            _LOGGER.warning("The socket stream expired, reconnecting")
            await self.close_socket()
            # add code to reconnect

    async def subscribe(self):
        """Subscribe to gateway output"""
        self._socket.send(b"subscribe(180)\n")

    async def close_socket(self):
        """Close socket connection"""
        self._socket.close()
        self._open = False

    async def async_get_data(self) -> dict:
        """Get data from the API."""
        return self._data

    async def run(self, tasks):
        """Run a specified list of tasks."""
        self.tasks = [asyncio.ensure_future(task) for task in tasks]
        try:
            await asyncio.gather(*self.tasks)
        except asyncio.TimeoutError:
            pass
        except Exception as other_exception:
            _LOGGER.error(
                f"Unexpected exception in connection: '{other_exception}'",
                exc_info=True,
            )
        finally:
            pass
