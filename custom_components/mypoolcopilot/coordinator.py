# coordinator.py
import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.core import HomeAssistant

from .const import DOMAIN, API_STATUS_URL, API_TOKEN_URL

_LOGGER = logging.getLogger(__name__)

class PoolCopilotDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, token_entity: str):
        super().__init__(
            hass,
            _LOGGER,
            name="MyPoolCopilot Coordinator",
            update_interval=timedelta(minutes=5),
        )
        self.token_entity = token_entity
        self.session = async_get_clientsession(hass)

    async def _async_update_data(self):
        if not self.token_entity:
            _LOGGER.error("❌ token_entity is None. Check your integration configuration.")
            raise UpdateFailed("token_entity is not configured")

        state = self.hass.states.get(self.token_entity)
        if not state:
            raise UpdateFailed(f"Entity '{self.token_entity}' not found")

        token = state.state
        headers = {
            "PoolCop-Token": token,
            "x-api-key": "a2AYWvjVYujm9I6q569j8PwpnJGXGczq",
        }

        try:
            async with self.session.get(API_STATUS_URL, headers=headers, timeout=10) as response:
                if response.status != 200:
                    raise UpdateFailed(f"Status request failed: {response.status}")
                data = await response.json()
                return data
        except Exception as err:
            raise UpdateFailed(f"Request error: {err}") from err

