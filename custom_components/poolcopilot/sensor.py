from __future__ import annotations

import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


def get_nested(data, path):
    """Accès récursif à une clé de type 'PoolCop.status.pump' dans un dict imbriqué."""
    for key in path.split('.'):
        if isinstance(data, dict):
            data = data.get(key)
        else:
            return None
    return data


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up PoolCopilot sensors from YAML."""
    coordinator = hass.data[DOMAIN]["coordinator"]

    sensors = [
        PoolCopilotSensor(coordinator, "PoolCop.temperature.water", "°C"),
        PoolCopilotSensor(coordinator, "PoolCop.temperature.air", "°C"),
        PoolCopilotSensor(coordinator, "PoolCop.pressure", "bar"),
        PoolCopilotSensor(coordinator, "PoolCop.pH", ""),
        PoolCopilotSensor(coordinator, "PoolCop.orp", "mV"),
        PoolCopilotSensor(coordinator, "PoolCop.ioniser", "A"),
        PoolCopilotSensor(coordinator, "PoolCop.voltage", "V"),
        PoolCopilotSensor(coordinator, "PoolCop.waterlevel", ""),
        PoolCopilotSensor(coordinator, "PoolCop.status.pump", ""),
        PoolCopilotSensor(coordinator, "PoolCop.status.pumpspeed", "%"),
        PoolCopilotSensor(coordinator, "PoolCop.status.valveposition", ""),
        PoolCopilotSensor(coordinator, "PoolCop.status.poolcop", ""),
    ]

    async_add_entities(sensors)


class PoolCopilotSensor(CoordinatorEntity, SensorEntity):
    """Representation of a PoolCopilot sensor."""

    def __init__(self, coordinator, key: str, unit: str):
        super().__init__(coordinator)
        self._key = key
        self._attr_native_unit_of_measurement = unit
        clean_key = key.replace("PoolCop.", "").replace(".", "_")
        self._attr_translation_key = f"poolcopilot_{clean_key}"
        self._attr_unique_id = self._attr_translation_key
        self._attr_native_unit_of_measurement = unit


    @property
    def native_value(self):
        """Return the value from nested data."""
        return get_nested(self.coordinator.data, self._key)

