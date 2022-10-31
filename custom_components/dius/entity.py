"""DiusEntity class"""
from custom_components.dius.enums import Msg_keys
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION
from .const import DOMAIN


class DiusEntity(CoordinatorEntity):

    _attr_has_entity_name = True

    def __init__(self, coordinator, config_entry, description):
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.entity_description = description

    @property
    def _attr_unique_id(self):
        """Return a unique ID to use for this entity."""
        data = self.coordinator.data.get(self.entity_description.key)
        return data.get(Msg_keys.mac.value)

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            configuration_url=ATTRIBUTION,
            identifiers={(DOMAIN, self._attr_unique_id)},
            name=self.entity_description.name,
            manufacturer=DOMAIN,
        )
