# __init__.py
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, PLATFORMS
from .coordinator import PoolCopilotDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up MyPoolCopilot from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    token_entity = entry.data.get("token_entity")
    coordinator = PoolCopilotDataUpdateCoordinator(hass, token_entity)
    hass.data[DOMAIN][entry.entry_id] = coordinator

    try:
        await coordinator.async_config_entry_first_refresh()
        _LOGGER.info("✅ Coordinator refreshed successfully at setup")
    except Exception as err:
        _LOGGER.warning("⚠ Initial data fetch failed: %s", err)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if DOMAIN in hass.data:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    if unload_ok:
        _LOGGER.debug("✅ Unload successful for  %s", entry.entry_id)
    else:
        _LOGGER.warning("⚠ unload_platforms returned False, but continuing to allow reload")
    return True

