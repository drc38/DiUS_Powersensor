"""DiusEntity class"""

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION
from .const import DOMAIN
from .enums import Msg_keys


class DiusEntity(CoordinatorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, config_entry, description):
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.entity_description = description
        data = self.coordinator.data.get(self.entity_description.key)
        self._attr_unique_id = data.get(Msg_keys.mac.value)

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            configuration_url=ATTRIBUTION,
            identifiers={(DOMAIN, self._attr_unique_id)},
            name=self.entity_description.name,
            manufacturer=DOMAIN,
        )
