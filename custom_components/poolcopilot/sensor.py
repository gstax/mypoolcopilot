from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Définition propre des sensors : clé JSON, unité, device_class
SENSORS = [
    {"key": "temperature_water", "device_class": "temperature", "unit": "°C"},
    {"key": "temperature_air", "device_class": "temperature", "unit": "°C"},
    {"key": "pressure", "device_class": "pressure", "unit": "bar"},
    {"key": "pH", "device_class": None, "unit": None},
    {"key": "orp", "device_class": None, "unit": "mV"},
    {"key": "ioniser", "device_class": None, "unit": None},
    {"key": "voltage", "device_class": "voltage", "unit": "V"},
    {"key": "waterlevel", "device_class": None, "unit": "%"},
    {"key": "status_pump", "device_class": None, "unit": None},
    {"key": "status_pumpspeed", "device_class": None, "unit": "%"},
    {"key": "status_valveposition", "device_class": None, "unit": None},
    {"key": "status_poolcop", "device_class": None, "unit": None},
]

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up PoolCopilot sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    _LOGGER.warning("PoolCopilot coordinator raw data: %s", coordinator.data)

    entities = []

    if coordinator.data:
        for sensor in SENSORS:
            key = sensor["key"]
            if key in coordinator.data:
                entities.append(PoolCopilotSensor(coordinator, sensor))
            else:
                _LOGGER.warning("Sensor key '%s' not found in API response", key)
    else:
        _LOGGER.warning("No data received from PoolCopilot API.")

    async_add_entities(entities)

class PoolCopilotSensor(CoordinatorEntity, SensorEntity):
    """Representation of a PoolCopilot sensor."""

    def __init__(self, coordinator, sensor: dict[str, Any]) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._key = sensor["key"]
        self._attr_unique_id = f"poolcopilot_{self._key}"
        self._attr_translation_key = f"poolcopilot_{self._key}"

        if sensor["device_class"]:
            self._attr_device_class = sensor["device_class"]

        if sensor["unit"]:
            self._attr_native_unit_of_measurement = sensor["unit"]

    @property
    def native_value(self) -> Any:
        """Return the sensor value."""
        return self.coordinator.data.get(self._key)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

