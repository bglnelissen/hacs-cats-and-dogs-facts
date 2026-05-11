from homeassistant.components.button import ButtonEntity
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
    async_add_entities([CatFactNextButton(coordinator, entry)])


class CatFactNextButton(CoordinatorEntity[CatFactsCoordinator], ButtonEntity):
    _attr_icon = "mdi:skip-next"
    _attr_has_entity_name = True
    _attr_name = "Next fact"

    def __init__(self, coordinator: CatFactsCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_next"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Cat Facts",
            "manufacturer": "bglnelissen",
            "model": "Cat Facts",
        }

    async def async_press(self) -> None:
        await self.coordinator.async_refresh()
