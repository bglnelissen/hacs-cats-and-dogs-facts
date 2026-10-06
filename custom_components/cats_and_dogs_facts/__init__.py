import logging
import random
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    DEFAULT_JSON_URL,
    DEFAULT_RANDOM,
    DEFAULT_UPDATE_INTERVAL,
    CONF_JSON_URL,
    CONF_RANDOM,
    CONF_UPDATE_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["sensor", "button"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coordinator = CatsAndDogsFactsCoordinator(hass, entry)
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        raise ConfigEntryNotReady from err
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_async_reload_entry))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def _async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


class CatsAndDogsFactsCoordinator(DataUpdateCoordinator[str]):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self._entry = entry
        self._facts: list[str] = []
        self._index: int = 0
        interval = timedelta(
            minutes=entry.options.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
        )
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=interval)

    async def _async_update_data(self) -> str:
        if not self._facts:
            await self._fetch_facts()
        if not self._facts:
            raise UpdateFailed("No facts available in the dataset")
        use_random = self._entry.options.get(CONF_RANDOM, DEFAULT_RANDOM)
        if use_random:
            return random.choice(self._facts)
        fact = self._facts[self._index % len(self._facts)]
        self._index += 1
        return fact

    async def _fetch_facts(self) -> None:
        url = self._entry.options.get(CONF_JSON_URL, DEFAULT_JSON_URL)
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(url, timeout=30) as resp:
                resp.raise_for_status()
                data = await resp.json(content_type=None)
        except Exception as err:
            raise UpdateFailed(f"Failed to fetch facts from {url}: {err}") from err

        if isinstance(data, list):
            self._facts = [f for f in data if isinstance(f, str)]
        elif isinstance(data, dict) and "facts" in data:
            self._facts = [f for f in data["facts"] if isinstance(f, str)]
        else:
            raise UpdateFailed(f"Unexpected JSON format at {url}")

        _LOGGER.debug("Loaded %d facts from %s", len(self._facts), url)
