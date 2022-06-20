"""Dius API Client."""
import asyncio
import json
import logging
import socket

from .enums import Msg_keys
from .enums import Msg_values


_LOGGER: logging.Logger = logging.getLogger(__package__)


class DiusApiClient:
    def __init__(self, host: str, port: int) -> None:
        """Dius API Client."""
        self._host = host
        self._port = port
        self._server_address = (host, port)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._open = False
        self._data = {}
        self._reconnects = 0
        self.tasks = None

    @staticmethod
    async def start(host: str, port: int):
        """Start socket and listen."""
        self = DiusApiClient(host, port)
        asyncio.create_task(self.run([self.open_socket(), self.listen()]))

        return self

    async def listen(self):
        """Listen for incoming messages."""
        while self._open:
            message, address = self._socket.recvfrom(1024)
            # _LOGGER.debug("Received message %s", message)
            await self.process_message(message)
            await asyncio.sleep(1)

    async def open_socket(self):
        """Open connection and subscribe to data."""
        self._socket.connect(self._server_address)
        self._open = True
        _LOGGER.info("The socket stream is connected, subscribing")
        while True:
            await self.subscribe()
            await asyncio.sleep(150)

    async def process_message(self, raw_msg):
        """Process json messages received."""
        msg = json.loads(raw_msg)
        _LOGGER.debug("Received message json: %s", msg)

        type = msg.get(Msg_keys.type.value)
        subtype = msg.get(Msg_keys.subtype.value)
        device = msg.get(Msg_keys.device.value)

        if type == Msg_values.instant_power.value:
            if device == Msg_values.sensor.value:
                self._data[Msg_values.sensor.value] = msg
            if device == Msg_values.plug.value:
                self._data[Msg_values.plug.value] = msg

        if (
            type == Msg_values.subscription.value
            and subtype == Msg_values.warning.value
        ):
            _LOGGER.warning("The socket stream had a warning, resubscribing")
            await self.subscribe()

        if type == Msg_values.subscription.value and subtype == Msg_values.expiry.value:
            _LOGGER.warning("The socket stream expired, reconnecting")
            await self.close_socket()
            # add code to reconnect

    async def subscribe(self):
        """Subscribe to gateway output."""
        self._socket.send(b"subscribe(180)\n")

    async def close_socket(self):
        """Close socket connection."""
        if self._socket:
            self._socket.close()
        self._open = False

    async def async_get_data(self) -> dict:
        """Get data from the API."""
        self._data.update({"reconnects": self._reconnects})
        return self._data

    async def run(self, tasks):
        """Run a specified list of tasks."""
        self.tasks = [asyncio.ensure_future(task) for task in tasks]
        try:
            await asyncio.gather(*self.tasks)
        except Exception as other_exception:
            _LOGGER.error(
                f"Unexpected exception in connection to '{self._host}': '{other_exception}'",
                exc_info=True,
            )
        finally:
            await self.stop()

    async def stop(self):
        """Close connection and cancel ongoing tasks."""
        await self.close_socket()
        for task in self.tasks:
            task.cancel()

    async def reconnect(self):
        """Reconnect to socket and listen."""
        if self._open is False:
            asyncio.create_task(self.run([self.open_socket(), self.listen()]))
            self._reconnects += 1
