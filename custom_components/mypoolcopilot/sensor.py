"""Sensor platform for MyPoolCopilot."""
from homeassistant.helpers.entity import Entity
from homeassistant.const import UnitOfTemperature
from .const import DOMAIN

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

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the MyPoolCopilot sensors."""
    data = hass.data[DOMAIN]
    sensors = []
    for key, value in SENSOR_TYPES.items():
        sensors.append(MyPoolCopilotSensor(data, key, value))
    async_add_entities(sensors, True)

class MyPoolCopilotSensor(Entity):
    """Representation of a MyPoolCopilot Sensor."""

    def __init__(self, data, key, description):
        """Initialize the sensor."""
        self._data = data
        self._key = key
        self._name = f"MyPoolCopilot {description['name']}"
        self._unit = description["unit"]
        self._state = None
        self._unique_id = f"mypoolcopilot_{key}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._unique_id

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    async def async_update(self):
        """Fetch new state data for the sensor."""
        await self._data.async_update()
        if self._data.data:
            self._state = self._data.data.get(self._key)

