from __future__ import annotations

import logging
from datetime import timedelta

import aiohttp
import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

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

    # 👉 Appel du setup de la plateforme "sensor"
    hass.async_create_task(
        async_load_platform(hass, "sensor", DOMAIN, {}, config)
    )

    return True

