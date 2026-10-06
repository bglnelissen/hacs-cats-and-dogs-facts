import re

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    CONF_JSON_URL,
    CONF_RANDOM,
    CONF_UPDATE_INTERVAL,
    DEFAULT_JSON_URL,
    DEFAULT_RANDOM,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
)

_INTERVAL_PATTERN = re.compile(r"(\d+)\s*([dhm])", re.IGNORECASE)
_MIN_MINUTES = 1
_MAX_MINUTES = 10080  # 7 days


def parse_interval(value: str) -> int:
    """Parse interval string (e.g. '6h', '1d', '30m', '1d6h') to minutes."""
    value = value.strip()
    if value.isdigit():
        return int(value) * 60  # bare number = hours
    total = 0
    for match in _INTERVAL_PATTERN.finditer(value):
        amount = int(match.group(1))
        unit = match.group(2).lower()
        if unit == "d":
            total += amount * 24 * 60
        elif unit == "h":
            total += amount * 60
        elif unit == "m":
            total += amount
    if total == 0:
        raise ValueError(f"Cannot parse: {value!r}")
    return total


def format_interval(minutes: int) -> str:
    """Format minutes to a human readable string like '6h' or '1d12h'."""
    if minutes < 60:
        return f"{minutes}m"
    hours, mins = divmod(minutes, 60)
    if hours < 24:
        return f"{hours}h{mins}m" if mins else f"{hours}h"
    days, hrs = divmod(hours, 24)
    return f"{days}d{hrs}h" if hrs else f"{days}d"


def _build_schema(defaults: dict) -> vol.Schema:
    current_minutes = defaults.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
    return vol.Schema(
        {
            vol.Optional(CONF_JSON_URL, default=defaults.get(CONF_JSON_URL, DEFAULT_JSON_URL)): selector.TextSelector(),
            vol.Optional(CONF_RANDOM, default=defaults.get(CONF_RANDOM, DEFAULT_RANDOM)): selector.BooleanSelector(),
            vol.Optional(CONF_UPDATE_INTERVAL, default=format_interval(current_minutes)): selector.TextSelector(),
        }
    )


def _validate_and_process(user_input: dict) -> tuple[dict, dict]:
    """Validate user input. Returns (processed_data, errors)."""
    errors = {}
    processed = dict(user_input)
    raw = user_input.get(CONF_UPDATE_INTERVAL, "")
    try:
        minutes = parse_interval(str(raw))
        if not (_MIN_MINUTES <= minutes <= _MAX_MINUTES):
            errors[CONF_UPDATE_INTERVAL] = "invalid_interval"
        else:
            processed[CONF_UPDATE_INTERVAL] = minutes
    except ValueError:
        errors[CONF_UPDATE_INTERVAL] = "invalid_interval"
    return processed, errors


class CatsAndDogsFactsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            processed, errors = _validate_and_process(user_input)
            if not errors:
                return self.async_create_entry(title="Cats and Dogs Facts", data={}, options=processed)
        return self.async_show_form(
            step_id="user",
            data_schema=_build_schema(user_input or {}),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return CatsAndDogsFactsOptionsFlow()


class CatsAndDogsFactsOptionsFlow(config_entries.OptionsFlow):
    async def async_step_init(self, user_input=None):
        errors = {}
        if user_input is not None:
            processed, errors = _validate_and_process(user_input)
            if not errors:
                return self.async_create_entry(data=processed)
        return self.async_show_form(
            step_id="init",
            data_schema=_build_schema(self.config_entry.options),
            errors=errors,
        )
