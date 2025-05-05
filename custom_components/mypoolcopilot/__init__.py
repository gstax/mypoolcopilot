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
        _LOGGER.debug("🔄 async_update_data() called")
        try:
            token_entity = hass.states.get("input_text.token_poolcopilot")
            if not token_entity:
                raise UpdateFailed("Token entity not found.")
            token = token_entity.state
            if not token or token in ("unknown", "unavailable"):
                raise UpdateFailed("Invalid token in input_text.token_poolcopilot.")
            with async_timeout.timeout(10):
                headers = {"PoolCop-Token": token}
                _LOGGER.debug("📡 Requesting /status with token: %s", token[:6] + "..." if token else "empty")
                async with session.get("https://poolcopilot.com/api/v1/status", headers=headers) as response:
                    _LOGGER.debug("✅ Received response: %s", response.status)
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
        _LOGGER.debug("⏳ Starting wait_for_token_and_refresh")
        while True:
            token_entity = hass.states.get("input_text.token_poolcopilot")
            if token_entity:
                _LOGGER.debug("🔍 token_entity found: %s", token_entity.state)
            else:
                _LOGGER.debug("❌ token_entity not found yet")

            if token_entity and token_entity.state not in ("unknown", "unavailable", ""):
                _LOGGER.info("🎯 Token is valid, triggering refresh")
                try:
                    await coordinator.async_refresh()
                    _LOGGER.info("✅ Coordinator refreshed successfully")
                    break
                except UpdateFailed as e:
                    _LOGGER.warning("⚠️ Refresh failed: %s", e)
            else:
                _LOGGER.debug("⌛ Waiting for valid token...")
            await asyncio.sleep(2)

    async def _handle_homeassistant_started_on_ready(hass: HomeAssistant):
        _LOGGER.debug("🚀 Setting up event listener for homeassistant_started")
        event = asyncio.Event()

        def _mark_ready(_):
            _LOGGER.debug("🏁 Home Assistant fully started")
            event.set()

        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, _mark_ready)
        await event.wait()
        await wait_for_token_and_refresh()

    hass.async_create_task(_handle_homeassistant_started_on_ready(hass))

    # ✅ Stocker le coordinator
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # ✅ Attendre le premier refresh avant de créer les entités
    await coordinator.async_config_entry_first_refresh()

    # ✅ Initialiser les plateformes (sensor.py)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

