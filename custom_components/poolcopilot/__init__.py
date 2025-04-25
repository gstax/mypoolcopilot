# __init__.py
from __future__ import annotations

import logging
from datetime import timedelta

import aiohttp
import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, API_STATUS_URL

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the PoolCopilot integration from configuration.yaml."""
    if DOMAIN not in config:
        return True

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["token"] = config[DOMAIN]["token"]

    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up PoolCopilot from a config entry."""
    session = aiohttp.ClientSession()

    async def async_update_data():
        """Fetch data from PoolCopilot."""
        try:
            with async_timeout.timeout(10):
                headers = {
                    "PoolCop-Token": hass.data[DOMAIN]["token"]
                }
                async with session.get(API_STATUS_URL, headers=headers) as response:
                    response.raise_for_status()
                    return await response.json()
        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="PoolCopilot",
        update_method=async_update_data,
        update_interval=timedelta(minutes=5),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN]["coordinator"] = coordinator

    return True

