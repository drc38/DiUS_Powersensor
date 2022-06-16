"""Tests for DiUS_Powersensor api."""
# import asyncio
# from custom_components.dius.api import (
#     DiusApiClient,
# )
# from custom_components.dius.const import (
#     CONF_HOST,
# )
# from custom_components.dius.const import (
#     CONF_PORT,
# )
from custom_components.dius.const import DOMAIN
from homeassistant import config_entries

from .const import MOCK_CONFIG
from .const import MOCK_OPTIONS


async def test_api(hass, caplog):
    """Test API calls."""
    # Initialize a config flow
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    # If a user were to enter form it would result in this function call
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=MOCK_CONFIG
    )
    entry = hass.config_entries.async_entries(DOMAIN)[0]
    result = await hass.config_entries.options.async_init(entry.entry_id)

    # Enter some fake data into the form
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input=MOCK_OPTIONS,
    )

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
