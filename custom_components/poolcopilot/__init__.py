from __future__ import annotations

import logging
from datetime import timedelta

import aiohttp
import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, API_STATUS_URL

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the PoolCopilot integration from configuration.yaml."""
    if DOMAIN not in config:
        return True

    hass.data.setdefault(DOMAIN, {})
    token = config[DOMAIN]["token"]

    session = aiohttp.ClientSession()

    async def async_update_data():
        try:
            with async_timeout.timeout(10):
                headers = {"PoolCop-Token": token}
                async with session.get(API_STATUS_URL, headers=headers) as response:
                    response.raise_for_status()
                    return await response.json()
        except Exception as err:
            raise UpdateFailed(f"Erreur lors de la récupération des données : {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="PoolCopilot",
        update_method=async_update_data,
        update_interval=timedelta(minutes=5),
    )

    await coordinator.async_refresh()
    hass.data[DOMAIN]["coordinator"] = coordinator

    # 👇 Appel direct à async_setup_platform avec async_add_entities correct
    from .sensor import async_setup_platform
    await async_setup_platform(hass, config, hass.helpers.entity_platform.async_add_entities)

    return True

