import logging
from datetime import timedelta
from typing import Any
import aiohttp

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, API_STATUS_URL

_LOGGER = logging.getLogger(__name__)

class PoolCopilotDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass, session: aiohttp.ClientSession, token_entity: str) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="MyPoolCopilot Coordinator",
            update_interval=timedelta(minutes=5),
        )
        self.session = session
        self.token_entity = token_entity

    async def _async_update_data(self) -> dict[str, Any]:
        if not self.token_entity:
            raise UpdateFailed("token_entity is not configured")

        state = self.hass.states.get(self.token_entity)
        if state is None:
            raise UpdateFailed(f"Token entity '{self.token_entity}' not found")

        token = state.state
        headers = {
            "PoolCop-Token": token,
            "x-api-key": "a2AYWvjVYujm9I6q569j8PwpnJGXGczq"
        }

        try:
            async with self.session.get(API_STATUS_URL, headers=headers, timeout=10) as response:
                if response.status != 200:
                    raise UpdateFailed(f"Status request failed: {response.status}")
                return await response.json()
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Client error: {err}")

