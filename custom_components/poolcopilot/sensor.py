from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up PoolCopilot sensors from YAML."""
    coordinator = hass.data[DOMAIN]["coordinator"]

    sensors = [
        PoolCopilotSensor(coordinator, "temperature.water", "Temperature Water", "°C"),
    ]

    async_add_entities(sensors)


class PoolCopilotSensor(CoordinatorEntity, SensorEntity):
    """Representation of a PoolCopilot sensor."""

    def __init__(self, coordinator, key, name, unit):
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._key)

