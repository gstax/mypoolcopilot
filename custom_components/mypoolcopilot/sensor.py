from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Liste complète : clé HA + chemin dans le JSON + device_class + unité
SENSORS = [
    {"key": "temperature_water", "path": ["PoolCop", "temperature", "water"], "device_class": "temperature", "unit": "°C"},
    {"key": "temperature_air", "path": ["PoolCop", "temperature", "air"], "device_class": "temperature", "unit": "°C"},
    {"key": "pressure", "path": ["PoolCop", "pressure"], "device_class": "pressure", "unit": "bar"},
    {"key": "pH", "path": ["PoolCop", "pH"], "device_class": None, "unit": None},
    {"key": "orp", "path": ["PoolCop", "orp"], "device_class": None, "unit": "mV"},
    {"key": "ioniser", "path": ["PoolCop", "ioniser"], "device_class": None, "unit": None},
    {"key": "voltage", "path": ["PoolCop", "voltage"], "device_class": "voltage", "unit": "V"},
    {"key": "waterlevel", "path": ["PoolCop", "waterlevel"], "device_class": None, "unit": "%"},
    {"key": "status_pump", "path": ["PoolCop", "status", "pump"], "device_class": None, "unit": None},
    {"key": "status_pumpspeed", "path": ["PoolCop", "status", "pumpspeed"], "device_class": None, "unit": "%"},
    {"key": "status_valveposition", "path": ["PoolCop", "status", "valveposition"], "device_class": None, "unit": None},
    {"key": "status_poolcop", "path": ["PoolCop", "status", "poolcop"], "device_class": None, "unit": None},
]

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up PoolCopilot sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    _LOGGER.warning("PoolCopilot coordinator raw data: %s", coordinator.data)

    entities = [PoolCopilotSensor(coordinator, sensor) for sensor in SENSORS]

    async_add_entities(entities)

class PoolCopilotSensor(CoordinatorEntity, SensorEntity):
    """Representation of a PoolCopilot sensor."""

    def __init__(self, coordinator, sensor: dict[str, Any]) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._key = sensor["key"]
        self._path = sensor["path"]
        self._attr_unique_id = self._key
        self._attr_translation_key = self._key

        if sensor["device_class"]:
            self._attr_device_class = sensor["device_class"]

        if sensor["unit"]:
            self._attr_native_unit_of_measurement = sensor["unit"]

    def _traverse_path(self, data: dict, path: list[str]) -> Any:
        """Traverse a dict following a path."""
        for elem in path:
            if not isinstance(data, dict) or elem not in data:
                return None
            data = data[elem]
        return data

    @property
    def native_value(self) -> Any:
        """Return the sensor value."""
        return self._traverse_path(self.coordinator.data, self._path)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

