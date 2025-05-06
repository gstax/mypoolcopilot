from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

import logging

_LOGGER = logging.getLogger(__name__)

SENSOR_KEYS = {
    "orp": "Redox (ORP)",
    "ph": "pH",
    "temperature": "Water Temperature",
    "pump_status": "Pump Status",
    "pump_speed": "Pump Speed",
    "valve_position": "Valve Position",
    "ioniser_status": "Ioniser Status",
    "poolcop_status": "System Status"
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = []
    for key, name in SENSOR_KEYS.items():
        if key in coordinator.data:
            sensors.append(PoolCopilotSensor(coordinator, key, name))
        else:
            _LOGGER.debug(f"Skipping sensor '{key}' – key not in data or no data yet")

    async_add_entities(sensors)
    _LOGGER.info("✅ All sensors added successfully")

class PoolCopilotSensor(SensorEntity):
    def __init__(self, coordinator, key, name):
        self._coordinator = coordinator
        self._key = key
        self._attr_name = f"PoolCopilot {name}"
        self._attr_unique_id = f"{DOMAIN}_{key}"

    @property
    def available(self):
        return self._key in self._coordinator.data

    @property
    def native_value(self):
        return self._coordinator.data.get(self._key)

    async def async_update(self):
        await self._coordinator.async_request_refresh()

