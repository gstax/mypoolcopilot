from __future__ import annotations

import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up PoolCopilot sensors from YAML."""
    coordinator = hass.data[DOMAIN]["coordinator"]

    _LOGGER.info("PoolCopilot sensors setup started")

    sensors = [
        PoolCopilotSensor(coordinator, "temperature.water", "Temperature Water", "°C"),
    ]

    await async_add_entities(sensors)


class PoolCopilotSensor(CoordinatorEntity, SensorEntity):
    """Representation of a PoolCopilot sensor."""

    def __init__(self, coordinator, key, name, unit):
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._attr_unique_id = f"poolcopilot_{key.replace('.', '_')}"

    @property
    def native_value(self):
        """Return the sensor value."""
        return self.coordinator.data.get(self._key)

