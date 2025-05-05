from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SENSORS = {
    "orp": {"name": "ORP", "unit": "mV"},
    "ph": {"name": "pH", "unit": None},
    "temperature": {"name": "Water Temperature", "unit": "°C"},
    "pump_status": {"name": "Pump Status", "unit": None},
    "pump_speed": {"name": "Pump Speed", "unit": "rpm"},
    "valve_position": {"name": "Valve Position", "unit": None},
    "ioniser_status": {"name": "Ioniser Status", "unit": None},
    "poolcop_status": {"name": "PoolCopilot Status", "unit": None},
}

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for key, description in SENSORS.items():
        if coordinator.data and key in coordinator.data:
            value = coordinator.data[key]
            _LOGGER.info("🔧 Adding sensor: %s = %s", key, value)
            entities.append(PoolCopilotSensor(coordinator, key, description))
        else:
            _LOGGER.debug("Skipping sensor '%s' – key not in data or no data yet", key)

    if entities:
        async_add_entities(entities)

class PoolCopilotSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, key: str, description: dict[str, Any]) -> None:
        super().__init__(coordinator)
        self._key = key
        self._attr_name = description["name"]
        self._attr_native_unit_of_measurement = description["unit"]
        self._attr_unique_id = key
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> Any:
        return self.coordinator.data.get(self._key)

