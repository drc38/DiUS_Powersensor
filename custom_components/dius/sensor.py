"""Sensor platform for DiUS_Powersensor."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.components.sensor import SensorStateClass

from .const import DOMAIN
from .const import MAIN_ICON
from .const import PLUG_ICON
from .const import SENSORS
from .const import W_to_U
from .entity import DiusEntity
from .enums import Msg_keys
from .enums import Msg_values


@dataclass
class DiusSensorDescription(SensorEntityDescription):
    """Class to describe a Sensor entity."""


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    for sens in SENSORS:
        if entry.options.get(sens) is True:
            desc = DiusSensorDescription(key=sens, name=sens)
            async_add_devices([DiusSensor(coordinator, entry, desc)], True)


class DiusSensor(DiusEntity, SensorEntity):
    """dius Sensor class."""

    entity_description: DiusSensorDescription

    def __init__(self, coordinator, config_entry, description: DiusSensorDescription):
        super().__init__(coordinator, config_entry)
        self.entity_description = description
        self._extra_attr = {}
        self._attr_name = ".".join([DOMAIN, self.entity_description.name])
        self.entity_id = DOMAIN + "." + self.entity_description.key
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._power: float | None = None

    @property
    def state(self):
        """Return the state of the sensor."""
        data = None
        if self.coordinator.data.get(self.entity_description.key) is not None:
            data = self.coordinator.data.get(self.entity_description.key)
            self._power = data.get(Msg_keys.power.value)
            if data.get(Msg_keys.unit, "") == "U":
                self._power = self._power / W_to_U
            self._power = round(self._power)
        return self._power

    @property
    def native_value(self):
        """Return the native measurement."""
        return self._power

    @property
    def icon(self):
        """Return the icon of the sensor."""
        if self.entity_description.key == Msg_values.plug.value:
            return PLUG_ICON
        if self.entity_description.key == Msg_values.sensor.value:
            return MAIN_ICON

    @property
    def native_unit_of_measurement(self):
        """Return the native unit of measurement."""
        return "W"

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self.coordinator.data.get(self.entity_description.key)

    @property
    def should_poll(self):
        """Return True if entity has to be polled for state.
        False if entity pushes its state to HA.
        """
        return True
