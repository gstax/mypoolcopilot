"""Sensor platform for MyPoolCopilot."""
import logging

from homeassistant.helpers.entity import Entity
from homeassistant.const import UnitOfTemperature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = {
    "air_temperature": {"name": "Air Temperature", "unit": UnitOfTemperature.CELSIUS},
    "ioniser_status": {"name": "Ioniser Status", "unit": None},
    "orp": {"name": "ORP", "unit": "mV"},
    "ph_level": {"name": "pH Level", "unit": None},
    "poolcop_status": {"name": "PoolCop Status", "unit": None},
    "pressure": {"name": "Pressure", "unit": "bar"},
    "pump_speed": {"name": "Pump Speed", "unit": "rpm"},
    "pump_status": {"name": "Pump Status", "unit": None},
    "valve_position": {"name": "Valve Position", "unit": None},
    "voltage": {"name": "Voltage", "unit": "V"},
    "water_level": {"name": "Water Level", "unit": "%"},
    "water_temperature": {"name": "Water Temperature", "unit": UnitOfTemperature.CELSIUS},
}

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up MyPoolCopilot sensors from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = [
        MyPoolCopilotSensor(coordinator, key, description)
        for key, description in SENSOR_TYPES.items()
    ]
    async_add_entities(sensors, True)

class MyPoolCopilotSensor(Entity):
    """Representation of a MyPoolCopilot Sensor."""

    def __init__(self, coordinator, key, description):
        self.coordinator = coordinator
        self._key = key
        self._name = description["name"]
        self._unit = description["unit"]
        self._unique_id = f"mypoolcopilot_{key}"
        self._attr_should_poll = False

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def state(self):
        return self.coordinator.data.get(self._key)

    @property
    def unit_of_measurement(self):
        return self._unit

    @property
    def available(self):
        return self.coordinator.last_update_success

    async def async_update(self):
        """Manually triggered update."""
        _LOGGER.debug(
            "[%s] Fetching state, coordinator data = %s",
            self._key,
            self.coordinator.data,
        )
        await self.coordinator.async_request_refresh()

