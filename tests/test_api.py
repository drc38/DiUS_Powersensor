"""Tests for DiUS_Powersensor api."""
import asyncio
import socket

from custom_components.dius import (
    async_setup_entry,
)
from custom_components.dius import (
    async_unload_entry,
)
from custom_components.dius.api import DiusApiClient
from custom_components.dius.const import DOMAIN
from pytest_homeassistant_custom_component.common import MockConfigEntry

from .const import CONF_HOST
from .const import CONF_PORT
from .const import MOCK_CONFIG_API
# from homeassistant import config_entries


# from custom_components.dius.api import (
#     DiusApiClient,
# )
# from custom_components.dius.const import (
#     CONF_HOST,
# )
# from custom_components.dius.const import (
#     CONF_PORT,
# )

# from .const import MOCK_OPTIONS


async def test_api(hass, caplog, socket_enabled):
    """Test API calls."""
    # Initialize a config flow
    # result = await hass.config_entries.flow.async_init(
    #    DOMAIN, context={"source": config_entries.SOURCE_USER}
    # )

    # If a user were to enter form it would result in this function call
    # result = await hass.config_entries.flow.async_configure(
    #    result["flow_id"], user_input=MOCK_CONFIG
    # )

    await SocketServer.start(CONF_HOST, CONF_PORT)

    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG_API, entry_id="testapi")
    await async_setup_entry(hass, config_entry)

    # await DiusApiClient.start(CONF_HOST, CONF_PORT)

    # await client.stop()
    # await server.stop()

    await async_unload_entry(hass, config_entry)

    # To test the api submodule, we first create an instance of our API client
    # api = DiusApiClient(MOCK_CONFIG[CONF_HOST], MOCK_CONFIG[CONF_PORT])

    # Use aioclient_mock which is provided by `pytest_homeassistant_custom_components`
    # to mock responses to aiohttp requests. In this case we are telling the mock to
    # return {"test": "test"} when a `GET` call is made to the specified URL. We then
    # call `async_get_data` which will make that `GET` request.

    # assert await api.async_get_data() == {"test": "test"}

    # We do the same for `async_set_title`. Note the difference in the mock call
    # between the previous step and this one. We use `patch` here instead of `get`
    # because we know that `async_set_title` calls `api_wrapper` with `patch` as the
    # first parameter

    # assert await api.async_set_title("test") is None

    # In order to get 100% coverage, we need to test `api_wrapper` to test the code
    # that isn't already called by `async_get_data` and `async_set_title`. Because the
    # only logic that lives inside `api_wrapper` that is not being handled by a third
    # party library (aiohttp) is the exception handling, we also want to simulate
    # raising the exceptions to ensure that the function handles them as expected.
    # The caplog fixture allows access to log messages in tests. This is particularly
    # useful during exception handling testing since often the only action as part of
    # exception handling is a logging statement
    # caplog.clear()
    # aioclient_mock.put(
    #     "https://jsonplaceholder.typicode.com/posts/1", exc=asyncio.TimeoutError
    # )
    # assert (
    #     await api.api_wrapper("put", "https://jsonplaceholder.typicode.com/posts/1")
    #     is None
    # )
    # assert (
    #     len(caplog.record_tuples) == 1
    #     and "Timeout error fetching information from" in caplog.record_tuples[0][2]
    # )

    # caplog.clear()
    # aioclient_mock.post(
    #     "https://jsonplaceholder.typicode.com/posts/1", exc=aiohttp.ClientError
    # )
    # assert (
    #     await api.api_wrapper("post", "https://jsonplaceholder.typicode.com/posts/1")
    #     is None
    # )
    # assert (
    #     len(caplog.record_tuples) == 1
    #     and "Error fetching information from" in caplog.record_tuples[0][2]
    # )

    # caplog.clear()
    # aioclient_mock.post("https://jsonplaceholder.typicode.com/posts/2", exc=Exception)
    # assert (
    #     await api.api_wrapper("post", "https://jsonplaceholder.typicode.com/posts/2")
    #     is None
    # )
    # assert (
    #     len(caplog.record_tuples) == 1
    #     and "Something really wrong happened!" in caplog.record_tuples[0][2]
    # )

    # caplog.clear()
    # aioclient_mock.post("https://jsonplaceholder.typicode.com/posts/3", exc=TypeError)
    # assert (
    #     await api.api_wrapper("post", "https://jsonplaceholder.typicode.com/posts/3")
    #     is None
    # )
    # assert (
    #     len(caplog.record_tuples) == 1
    #     and "Error parsing information from" in caplog.record_tuples[0][2]
    # )


class SocketServer:
    """Test socket server for api."""

    def __init__(self, host: str, port: int):
        """Init extra variables for testing."""
        self.accept: bool = True
        self._server_address = (host, port)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._conn = None

    @staticmethod
    async def start(host: str, port: int):
        """Start socket and listen."""
        self = SocketServer(host, port)
        asyncio.create_task(self.run([self.listen()]))

        return self

    async def listen(self):
        """Listen for incoming messages."""
        with self._socket as s:
            s.bind(self._server_address)
            s.listen()
            self._conn, addr = s.accept()
            # with self._conn:
            while True:
                await asyncio.sleep(1)
                data, self._conn = s.recvfrom(1024)
                # if data:
                # self._conn.sendall(data)

    async def send_message(self):
        """Send test messages."""
        sensor_data = {
            "mac": "2cf4320aaaa",
            "device": "sensor",
            "summation": 21931891707,
            "duration": 30,
            "type": "instant_power",
            "batteryMicrovolt": 4143072,
            "unit": "U",
            "starttime": 1653477217,
            "power": 93184,
        }
        self._socket.sendto(sensor_data, self._conn)

    async def run(self, tasks):
        """Run a specified list of tasks."""
        self.tasks = [asyncio.ensure_future(task) for task in tasks]
        try:
            await asyncio.gather(*self.tasks)
        except Exception:  # as other_exception:
            pass
            # _LOGGER.error(
            #     f"Unexpected exception in connection to '{self._host}': '{other_exception}'",
            #     exc_info=True,
            # )
        finally:
            await self.stop()

    async def stop(self):
        """Close connection and cancel ongoing tasks."""
        await self.close_socket()
        for task in self.tasks:
            task.cancel()

    async def close_socket(self):
        """Close socket connection."""
        if self._socket:
            self._socket.close()
