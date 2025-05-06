from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SENSOR_KEYS = [
    "orp",
    "ph",
    "temperature",
    "pump_status",
    "pump_speed",
    "valve_position",
    "ioniser_status",
    "poolcop_status",
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up PoolCopilot sensors based on a config entry."""
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = []
    for key in SENSOR_KEYS:
        if key not in coordinator.data:
            _LOGGER.debug("Skipping sensor '%s' – key not in data or no data yet", key)
            continue
        sensors.append(PoolCopilotSensor(coordinator, key))
        _LOGGER.debug("✅ Added sensor for key '%s'", key)

    async_add_entities(sensors)
    _LOGGER.info("✅ All sensors added successfully")


class PoolCopilotSensor(SensorEntity):
    """Representation of a PoolCopilot sensor."""

    def __init__(self, coordinator: DataUpdateCoordinator, key: str) -> None:
        self._coordinator = coordinator
        self._key = key
        self._attr_name = f"PoolCopilot {key.replace('_', ' ').title()}"
        self._attr_unique_id = f"{DOMAIN}_{key}"
        _LOGGER.debug("Initialized PoolCopilotSensor for key '%s'", key)

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def available(self) -> bool:
        return self._key in self._coordinator.data

    @property
    def native_value(self) -> Any:
        value = self._coordinator.data.get(self._key)
        _LOGGER.debug("Sensor '%s' value: %s", self._key, value)
        return value

    async def async_added_to_hass(self) -> None:
        self._coordinator.async_add_listener(self.async_write_ha_state)

