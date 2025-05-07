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
        errors = {}

        if user_input is not None:
            apikey = user_input.get("apikey")
            if not apikey:
                errors["base"] = "missing_apikey"
            else:
                return self.async_create_entry(
                    title="PoolCopilot",
                    data={
                        "apikey": apikey,
                        "token_entity": "input_text.token_poolcopilot",  # ✅ Ajout ici
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("apikey"): str,
            }),
            errors=errors,
        )

