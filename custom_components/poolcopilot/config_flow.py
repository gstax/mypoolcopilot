from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

class PoolCopilotConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for PoolCopilot."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle a flow initiated by the user."""
        if user_input is not None:
            return self.async_create_entry(title="My PoolCopilot", data={})

        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))

