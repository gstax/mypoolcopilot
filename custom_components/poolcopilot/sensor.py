# sensor.py
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup PoolCopilot sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    # Liste des sensors à créer
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

