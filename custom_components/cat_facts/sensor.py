from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import CatFactsCoordinator
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: CatFactsCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([CatFactSensor(coordinator, entry)])


class CatFactSensor(CoordinatorEntity[CatFactsCoordinator], SensorEntity):
    _attr_icon = "mdi:cat"
    _attr_has_entity_name = True
    _attr_name = "Fact"

    def __init__(self, coordinator: CatFactsCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_fact"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Cat Facts",
            "manufacturer": "bglnelissen",
            "model": "Cat Facts",
        }

    @property
    def native_value(self) -> str | None:
        fact = self.coordinator.data
        if fact is None:
            return None
        if len(fact) <= 255:
            return fact
        return fact[:254] + "…"  # … as single char to stay within 255

    @property
    def extra_state_attributes(self) -> dict:
        return {"fact": self.coordinator.data}
