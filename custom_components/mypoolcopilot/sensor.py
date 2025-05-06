from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import MyPoolCopilotCoordinator
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SENSOR_KEYS = {
    "orp": "ORP",
    "ph": "pH",
    "temperature": "Water Temperature",
    "pump_status": "Pump Status",
    "pump_speed": "Pump Speed",
    "valve_position": "Valve Position",
    "ioniser_status": "Ioniser Status",
    "poolcop_status": "PoolCop Status",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: MyPoolCopilotCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    data = coordinator.data
    if not data:
        _LOGGER.warning("🚫 No data available yet, no sensors created")
        return

    for key, name in SENSOR_KEYS.items():
        if key in data:
            _LOGGER.debug("✅ Adding sensor '%s' with value: %s", key, data[key])
            entities.append(MyPoolCopilotSensor(coordinator, key, name))
        else:
            _LOGGER.debug("⏭ Skipping sensor '%s' – key not found in data", key)

    async_add_entities(entities)
    _LOGGER.info("🆗 %d sensor(s) added for PoolCopilot", len(entities))


class MyPoolCopilotSensor(CoordinatorEntity, SensorEntity):
    def __init__(
        self,
        coordinator: MyPoolCopilotCoordinator,
        key: str,
        name: str,
    ) -> None:
        super().__init__(coordinator)
        self._key = key
        self._attr_name = f"PoolCopilot {name}"
        self._attr_unique_id = f"mypoolcopilot_{key}"
        _LOGGER.debug("🔧 Created sensor entity: %s", self._attr_name)

    @property
    def native_value(self) -> Any:
        value = self.coordinator.data.get(self._key)
        _LOGGER.debug("📥 native_value for %s: %s", self._attr_name, value)
        return value

