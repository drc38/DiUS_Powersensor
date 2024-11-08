"""Constants for DiUS_Powersensor."""

from .enums import Msg_values

# Base component constants
NAME = "DiUS_Powersensor"
DOMAIN = "dius"
DOMAIN_DATA = f"{DOMAIN}_data"

ATTRIBUTION = "https://www.powersensor.com.au/"
ISSUE_URL = "https://github.com/drc38/DiUS_Powersensor/issues"

# Icons
MAIN_ICON = "mdi:home-lightning-bolt-outline"
PLUG_ICON = "mdi:power-plug-outline"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
SWITCH = "switch"
PLATFORMS = [SENSOR]

# Sensors
PLUG = Msg_values.plug.value
MAIN_POWER = Msg_values.sensor.value
SENSORS = [MAIN_POWER, PLUG]


# Configuration and options
CONF_ENABLED = "enabled"
CONF_HOST = "host"
CONF_PORT = "port"
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 49476

# Defaults
DEFAULT_NAME = DOMAIN

# Conversion
U_CONV = "U_conv"
DEFAULT_W_to_U = 19.3
W_ADJ = "W_adj"
DEFAULT_W_ADJ = 0

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
