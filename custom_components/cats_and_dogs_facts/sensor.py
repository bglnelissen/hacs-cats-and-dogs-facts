from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import CatsAndDogsFactsCoordinator
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: CatsAndDogsFactsCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([CatsAndDogsFactSensor(coordinator, entry)])


class CatsAndDogsFactSensor(CoordinatorEntity[CatsAndDogsFactsCoordinator], SensorEntity):
    _attr_icon = "mdi:paw"
    _attr_has_entity_name = True
    _attr_name = "Fact"

    def __init__(self, coordinator: CatsAndDogsFactsCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_fact"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Cats and Dogs Facts",
            "manufacturer": "bglnelissen",
            "model": "Cats and Dogs Facts",
        }

    @property
    def native_value(self) -> str | None:
        return self.coordinator.data

    @property
    def extra_state_attributes(self) -> dict:
        return {"fact": self.coordinator.data}
