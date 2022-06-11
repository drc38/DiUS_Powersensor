"""Additional enumerated values to use in home assistant."""
from enum import Enum, IntFlag, auto


class Msg_keys(str, Enum):
    """Message keys from sensor."""

    active_current = "active_current"
    batteryMicrovolt = "batteryMicrovolt"
    count = "count"
    current = "current"
    device = "device"
    duration = "duration"
    mac = "mac"
    power = "power"
    reactive_current = "reactive_current"
    source = "source"
    starttime = "starttime"
    subtype = "subtype"
    summation = "summation"
    type = "type"
    unit = "unit"
    voltage = "voltage"
    
    
class Msg_values(str, Enum):
    """Message values from sensor."""

    BLE = "BLE"
    expiry = "expiry"
    instant_power = "instant_power"
    plug = "plug"
    sensor = "sensor"
    subscription = "subscription"
    U = "U"
    W = "W"
    warning = "warning"