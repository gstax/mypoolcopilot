from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

SENSORS = {
    "orp": ("ORP", "mV"),
    "ph_level": ("pH Level", None),
    "pressure": ("Pressure", "bar"),
    "water_level": ("Water Level", "%"),
    "water_temperature": ("Water Temperature", "°C"),
    "air_temperature": ("Air Temperature", "°C"),
    "ioniser_status": ("Ioniser Status", None),
    "pump_status": ("Pump Status", None),
    "pump_speed": ("Pump Speed", "rpm"),
    "valve_position": ("Valve Position", None),
    "poolcop_status": ("PoolCop Status", None),
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    for key, (name, unit) in SENSORS.items():
        entities.append(PoolCopilotSensor(coordinator, key, name, unit))

    async_add_entities(entities)

class PoolCopilotSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, key, name, unit):
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._attr_unique_id = key
        self._attr_has_entity_name = True

    @property
    def native_value(self):
        return self.coordinator.data.get(self._key)

