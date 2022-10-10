"""Constants for DiUS_Powersensor tests."""
from custom_components.dius.const import (
    CONF_HOST,
)
from custom_components.dius.const import (
    CONF_PORT,
)

MOCK_CONFIG_API = {CONF_HOST: "127.0.0.1", CONF_PORT: 49476}
MOCK_CONFIG = {CONF_HOST: "192.168.1.1", CONF_PORT: 6789}
MOCK_OPTIONS = {"sensor": True, "plug": False, "U_conv": 32.1, "W_adj": -125}
