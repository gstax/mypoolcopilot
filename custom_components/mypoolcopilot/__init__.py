import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.exceptions import ConfigEntryNotReady
from .const import DOMAIN, PLATFORMS
from .coordinator import PoolCopilotDataUpdateCoordinator
from homeassistant.helpers.update_coordinator import UpdateFailed

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up MyPoolCopilot from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    session = async_get_clientsession(hass)
    token_entity = entry.data.get("token_entity")

    coordinator = PoolCopilotDataUpdateCoordinator(hass, session, token_entity)
    hass.data[DOMAIN][entry.entry_id] = coordinator

    try:
        await coordinator.async_config_entry_first_refresh()
        _LOGGER.info("✅ Coordinator refreshed successfully at setup")
    except UpdateFailed as err:
        _LOGGER.warning("⚠ Initial data fetch failed: %s", err)

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
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

