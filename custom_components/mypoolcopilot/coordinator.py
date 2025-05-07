import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from aiohttp import ClientSession

from .const import DOMAIN, API_STATUS_URL, API_TOKEN_URL

_LOGGER = logging.getLogger(__name__)

class PoolCopilotDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, session: ClientSession, token_entity: str) -> None:
        """Initialize coordinator."""
        self.hass = hass
        self.session = session
        self.token_entity = token_entity
        self.api_key = None
        self.token = None

        super().__init__(
            hass,
            _LOGGER,
            name="MyPoolCopilot Coordinator",
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from PoolCopilot."""
        _LOGGER.debug("🔄 Fetching PoolCopilot data")

        # Lire le token depuis l'entité input_text
        state = self.hass.states.get(self.token_entity)
        if not state:
            raise UpdateFailed(f"State for token entity {self.token_entity} not found")

        self.token = state.state.strip()
        _LOGGER.debug("🔐 Current token: %s", self.token)

        if not self.token:
            raise UpdateFailed("Token is empty")

        # Obtenir l'API key depuis le token JWT décodé
        self.api_key = await self._get_api_key_from_token()
        if not self.api_key:
            raise UpdateFailed("API key could not be determined")

        _LOGGER.debug("🔑 Using API key: %s", self.api_key)

        headers = {
            "PoolCop-Token": self.token,
            "x-api-key": self.api_key,
        }

        try:
            response = await self.session.get(API_STATUS_URL, headers=headers)
            if response.status != 200:
                _LOGGER.warning("⚠️ PoolCopilot API returned HTTP %s", response.status)
                raise UpdateFailed(f"Status request failed with code {response.status}")

            data = await response.json()
            _LOGGER.debug("📦 PoolCopilot response: %s", data)

            return data

        except Exception as err:
            _LOGGER.exception("❌ Exception while fetching PoolCopilot data: %s", err)
            raise UpdateFailed(f"Error fetching PoolCopilot data: {err}")

    async def _get_api_key_from_token(self) -> str | None:
        """Decode token to extract API key."""
        if not self.token or "." not in self.token:
            _LOGGER.warning("⚠️ Invalid token format")
            return None

        try:
            import base64
            import json

            payload_b64 = self.token.split(".")[1]
            padding = "=" * (-len(payload_b64) % 4)
            payload_bytes = base64.urlsafe_b64decode(payload_b64 + padding)
            payload = json.loads(payload_bytes.decode("utf-8"))
            return payload.get("apiKey") or payload.get("apikey")

        except Exception as err:
            _LOGGER.warning("⚠️ Failed to decode token payload: %s", err)
            return None

