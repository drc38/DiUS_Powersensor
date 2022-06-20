"""Global fixtures for DiUS_Powersensor integration."""
from unittest.mock import patch

import pytest
from custom_components.dius.api import (
    DiusApiClient,
)

pytest_plugins = "pytest_homeassistant_custom_component"


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations defined in the test dir."""
    yield


# This fixture is used to prevent HomeAssistant from attempting to create and dismiss persistent
# notifications. These calls would fail without this fixture since the persistent_notification
# integration is never loaded during a test.
@pytest.fixture(name="skip_notifications", autouse=True)
def skip_notifications_fixture():
    """Skip notification calls."""
    with patch("homeassistant.components.persistent_notification.async_create"), patch(
        "homeassistant.components.persistent_notification.async_dismiss"
    ):
        yield


# This fixture, when used, will result in skipping calls to api.start.
@pytest.fixture(name="skip_api_start")
def skip_api_start(socket_enabled):
    """Skip start calls."""
    with patch(
        "custom_components.dius.DiusApiClient.start",
        return_value=DiusApiClient("127.0.0.1", 1234),
    ):
        yield


# This fixture, when used, will result in calls to async_get_data to return None. To have the call
# return a value, we would add the `return_value=<VALUE_TO_RETURN>` parameter to the patch call.
@pytest.fixture(name="bypass_get_data")
def bypass_get_data_fixture():
    """Skip calls to get data from API."""
    with patch("custom_components.dius.DiusApiClient.async_get_data"):
        yield


# In this fixture, we are forcing calls to async_get_data to raise an Exception. This is useful
# for exception handling.
@pytest.fixture(name="error_on_get_data")
def error_get_data_fixture():
    """Simulate error when retrieving data from API."""
    with patch(
        "custom_components.dius.DiusApiClient.async_get_data", side_effect=Exception
        ), patch(
        "custom_components.dius.config_flow.DiusFlowHandler._test_credentials",
        return_value=False,
    ):
        yield
