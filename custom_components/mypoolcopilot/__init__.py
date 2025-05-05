from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

import asyncio
from aiohttp import ClientError
import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up PoolCopilot from a config entry."""
    session = async_get_clientsession(hass)

    async def async_update_data() -> dict[str, Any]:
        try:
            token_entity = hass.states.get("input_text.token_poolcopilot")
            if not token_entity:
                raise UpdateFailed("Token entity not found.")
            token = token_entity.state
            if not token or token in ("unknown", "unavailable"):
                raise UpdateFailed("Invalid token in input_text.token_poolcopilot.")
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

    async def wait_for_token_and_refresh():
        while True:
            token_entity = hass.states.get("input_text.token_poolcopilot")
            if token_entity and token_entity.state not in ("unknown", "unavailable", ""):
                try:
                    await coordinator.async_refresh()
                    _LOGGER.info("Coordinator refreshed after token became available.")
                    break
                except UpdateFailed as e:
                    _LOGGER.warning("Refresh failed after token ready: %s", e)
            else:
                _LOGGER.debug("Waiting for token entity to become available...")
                await asyncio.sleep(2)

    async def _handle_homeassistant_started_on_ready(hass: HomeAssistant):
        event = asyncio.Event()

        def _mark_ready(_):
            event.set()

        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, _mark_ready)
        await event.wait()
        await wait_for_token_and_refresh()

    hass.async_create_task(_handle_homeassistant_started_on_ready(hass))
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

