import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    DOMAIN,
    DEFAULT_JSON_URL,
    DEFAULT_RANDOM,
    DEFAULT_UPDATE_INTERVAL,
    CONF_JSON_URL,
    CONF_RANDOM,
    CONF_UPDATE_INTERVAL,
)


def _options_schema(defaults: dict) -> vol.Schema:
    return vol.Schema(
        {
            vol.Optional(CONF_JSON_URL, default=defaults.get(CONF_JSON_URL, DEFAULT_JSON_URL)): str,
            vol.Optional(CONF_RANDOM, default=defaults.get(CONF_RANDOM, DEFAULT_RANDOM)): bool,
            vol.Optional(
                CONF_UPDATE_INTERVAL,
                default=defaults.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL),
            ): vol.All(int, vol.Range(min=1, max=168)),
        }
    )


class CatFactsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Cat Facts", data={}, options=user_input)
        return self.async_show_form(
            step_id="user",
            data_schema=_options_schema({}),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return CatFactsOptionsFlow()


class CatFactsOptionsFlow(config_entries.OptionsFlow):
    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(data=user_input)
        return self.async_show_form(
            step_id="init",
            data_schema=_options_schema(self.config_entry.options),
        )
