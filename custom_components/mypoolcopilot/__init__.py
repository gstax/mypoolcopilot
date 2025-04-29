from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

import asyncio
from aiohttp import ClientError
import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up PoolCopilot from a config entry."""
    session = async_get_clientsession(hass)
    apikey = entry.data["apikey"]

    async def async_update_data() -> dict[str, Any]:
        """Fetch data from PoolCopilot API."""

        try:
            # 1. Récupérer un nouveau token
            with async_timeout.timeout(10):
                headers = {"Content-Type": "application/x-www-form-urlencoded"}
                payload = f"APIKEY={apikey}"
                async with session.post("https://poolcopilot.com/api/v1/token", headers=headers, data=payload) as response:
                    response.raise_for_status()
                    result = await response.json()
                    token = result.get("token")
                    if not token:
                        raise UpdateFailed("Token not received from PoolCopilot API.")

            # 2. Interroger /status avec ce token
            with async_timeout.timeout(10):
                headers = {"PoolCop-Token": token}
                async with session.get("https://poolcopilot.com/api/v1/status", headers=headers) as response:
                    response.raise_for_status()
                    return (await response.json()).get("data", {})  # ✅ ici on extrait bien la partie utile

        except (ClientError, asyncio.TimeoutError) as err:
            raise UpdateFailed(f"Error fetching PoolCopilot data: {err}") from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="PoolCopilot",
        update_method=async_update_data,
        update_interval=timedelta(minutes=5),
    )

    await coordinator.async_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

