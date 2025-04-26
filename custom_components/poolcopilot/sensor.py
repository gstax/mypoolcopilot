from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Liste fixe des sensors à créer
SENSOR_KEYS = [
    "temperature_water",
    "temperature_air",
    "pressure",
    "pH",
    "orp",
    "ioniser",
    "voltage",
    "waterlevel",
    "status_pump",
    "status_pumpspeed",
    "status_valveposition",
    "status_poolcop",
]

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up PoolCopilot sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    _LOGGER.debug("PoolCopilot coordinator data: %s", coordinator.data)

    entities = []

    if coordinator.data:
        for key in SENSOR_KEYS:
            if key in coordinator.data:
                entities.append(PoolCopilotSensor(coordinator, key))
            else:
                _LOGGER.warning("Sensor key '%s' not found in API response", key)
    else:
        _LOGGER.warning("No data received from PoolCopilot API.")

    async_add_entities(entities)

class PoolCopilotSensor(CoordinatorEntity, SensorEntity):
    """Representation of a PoolCopilot sensor."""

    def __init__(self, coordinator, key: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._key = key
        self._attr_unique_id = f"poolcopilot_{key}"
        self._attr_translation_key = f"poolcopilot_{key}"

    @property
    def native_value(self) -> Any:
        """Return the sensor value."""
        return self.coordinator.data.get(self._key)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

