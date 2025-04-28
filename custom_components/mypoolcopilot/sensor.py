"""Sensor platform for MyPoolCopilot."""
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

# Définition des capteurs disponibles
SENSOR_TYPES = [
    ("temperature_water", "Water Temperature", "°C", "temperature"),
    ("temperature_air", "Air Temperature", "°C", "temperature"),
    ("pressure", "Pressure", "bar", "pressure"),
    ("pH", "pH Level", None, None),
    ("orp", "ORP", "mV", None),
    ("ioniser", "Ioniser Status", None, None),
    ("voltage", "Voltage", "V", "voltage"),
    ("waterlevel", "Water Level", "%", None),
    ("status_pump", "Pump Status", None, None),
    ("status_pumpspeed", "Pump Speed", "%", None),
    ("status_valveposition", "Valve Position", None, None),
    ("status_poolcop", "PoolCop Status", None, None),
]


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up MyPoolCopilot sensors from a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    sensors = []

    for sensor_type, name, unit, device_class in SENSOR_TYPES:
        sensors.append(
            MyPoolCopilotSensor(coordinator, sensor_type, name, unit, device_class)
        )

    async_add_entities(sensors)


class MyPoolCopilotSensor(CoordinatorEntity, SensorEntity):
    """Representation of a MyPoolCopilot Sensor."""

    def __init__(self, coordinator, sensor_type, name, unit, device_class):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_unique_id = sensor_type
        self._attr_translation_key = sensor_type

    @property
    def native_value(self):
        """Return the sensor value."""
        return self.coordinator.data.get(self._sensor_type)

