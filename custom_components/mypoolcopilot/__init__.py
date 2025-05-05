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

    async def async_update_data() -> dict[str, Any]:
        """Fetch data from PoolCopilot API."""
        try:
            # 1. Récupérer le token depuis l'entité input_text
            token_entity = hass.states.get("input_text.token_poolcopilot")
            if not token_entity:
                raise UpdateFailed("Token entity not found.")
            token = token_entity.state
            if not token or token in ("unknown", "unavailable"):
                raise UpdateFailed("Invalid token in input_text.token_poolcopilot.")

            # 2. Interroger /status avec ce token
            with async_timeout.timeout(10):
                headers = {"PoolCop-Token": token}
                async with session.get("https://poolcopilot.com/api/v1/status", headers=headers) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"Status request failed: {response.status}")
                    return await response.json()

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

