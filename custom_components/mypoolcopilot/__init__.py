import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN
from .coordinator import PoolCopilotDataUpdateCoordinator

PLATFORMS = ["sensor"]

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up MyPoolCopilot from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    token_entity = entry.data.get("token_entity")
    apikey = entry.data.get("apikey")

    if not token_entity or not apikey:
        _LOGGER.error("❌ 'token_entity' or 'apikey' is missing from config entry data")
        raise ConfigEntryNotReady("'token_entity' or 'apikey' is missing")

    session = async_get_clientsession(hass)
    coordinator = PoolCopilotDataUpdateCoordinator(hass, session, token_entity, apikey)
    await coordinator.async_config_entry_first_refresh()
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

