# coordinator.py
import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, API_STATUS_URL
import aiohttp

_LOGGER = logging.getLogger(__name__)

class PoolCopilotDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, session: aiohttp.ClientSession, token_entity: str):
        self.hass = hass
        self.session = session
        self.token_entity = token_entity

        super().__init__(
            hass,
            _LOGGER,
            name="MyPoolCopilot Coordinator",
            update_interval=timedelta(minutes=1),
        )

    async def _async_update_data(self):
        try:
            token = self.hass.states.get(self.token_entity)
            if not token:
                raise UpdateFailed(f"Token entity '{self.token_entity}' not found")

            token_value = token.state
            headers = {"Authorization": f"Bearer {token_value}"}
            async with self.session.get(API_STATUS_URL, headers=headers) as response:
                if response.status != 200:
                    raise UpdateFailed(f"Status request failed: {response.status}")
                return await response.json()
        except Exception as err:
            raise UpdateFailed(f"Error fetching PoolCopilot data: {err}")

