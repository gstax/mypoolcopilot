"""Sensor platform for MyPoolCopilot integration."""

from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import UnitOfTemperature, UnitOfPressure, UnitOfElectricPotential, PERCENTAGE

from .const import DOMAIN

SENSOR_TYPES = {
    "temperature_air": {
        "name": "Air Temperature",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "unit_of_measurement": UnitOfTemperature.CELSIUS,
    },
    "temperature_water": {
        "name": "Water Temperature",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "unit_of_measurement": UnitOfTemperature.CELSIUS,
    },
    "pressure": {
        "name": "Pressure",
        "device_class": SensorDeviceClass.PRESSURE,
        "unit_of_measurement": UnitOfPressure.BAR,
    },
    "pH": {
        "name": "pH Level",
        "device_class": None,
        "unit_of_measurement": None,
    },
    "orp": {
        "name": "ORP",
        "device_class": None,
        "unit_of_measurement": "mV",
    },
    "ioniser": {
        "name": "Ioniser Status",
        "device_class": None,
        "unit_of_measurement": None,
    },
    "voltage": {
        "name": "Voltage",
        "device_class": SensorDeviceClass.VOLTAGE,
        "unit_of_measurement": UnitOfElectricPotential.VOLT,
    },
    "waterlevel": {
        "name": "Water Level",
        "device_class": None,
        "unit_of_measurement": PERCENTAGE,
    },
    "status_pump": {
        "name": "Pump Status",
        "device_class": None,
        "unit_of_measurement": None,
    },
    "status_pumpspeed": {
        "name": "Pump Speed",
        "device_class": None,
        "unit_of_measurement": PERCENTAGE,
    },
    "status_valveposition": {
        "name": "Valve Position",
        "device_class": None,
        "unit_of_measurement": None,
    },
    "status_poolcop": {
        "name": "PoolCop Status",
        "device_class": None,
        "unit_of_measurement": None,
    },
}

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up MyPoolCopilot sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for key, description in SENSOR_TYPES.items():
        entities.append(MyPoolCopilotSensor(coordinator, key, description))

    async_add_entities(entities)

class MyPoolCopilotSensor(SensorEntity):
    """Representation of a MyPoolCopilot sensor."""

    def __init__(self, coordinator, key, description):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self.key = key
        self._attr_name = description["name"]
        self._attr_unique_id = f"mypoolcopilot_{key}"
        self._attr_device_class = description["device_class"]
        self._attr_native_unit_of_measurement = description["unit_of_measurement"]

    @property
    def available(self):
        """Return True if entity is available."""
        return self.coordinator.last_update_success

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("mypoolcopilot", {}).get(self.key)

    async def async_update(self):
        """Update the entity."""
        await self.coordinator.async_request_refresh()

