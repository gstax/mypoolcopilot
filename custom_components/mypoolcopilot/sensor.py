import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SENSOR_DEFINITIONS = {
    "orp": {"name": "ORP", "unit": "mV", "path": "PoolCop.orp"},
    "ph": {"name": "pH", "unit": "", "path": "PoolCop.pH"},
    "temperature": {"name": "Water Temperature", "unit": "°C", "path": "PoolCop.temperature.water"},
    "air_temperature": {"name": "Air Temperature", "unit": "°C", "path": "PoolCop.temperature.air"},
    "pressure": {"name": "Water Pressure", "unit": "bar", "path": "PoolCop.pressure"},
    "voltage": {"name": "Voltage", "unit": "V", "path": "PoolCop.voltage"},
    "water_level": {"name": "Water Level", "unit": "", "path": "PoolCop.waterlevel"},
    "pump_status": {"name": "Pump Status", "unit": "", "path": "PoolCop.status.pump"},
    "pump_speed": {"name": "Pump Speed", "unit": "", "path": "PoolCop.status.pumpspeed"},
    "valve_position": {"name": "Valve Position", "unit": "", "path": "PoolCop.status.valveposition"},
    "ioniser_status": {"name": "Ioniser Status", "unit": "", "path": "PoolCop.status.ioniser"},
    "poolcop_status": {"name": "PoolCop Status", "unit": "", "path": "PoolCop.status.poolcop"},
}


def get_value_from_path(data, path):
    try:
        for key in path.split("."):
            data = data[key]
        return data
    except (KeyError, TypeError):
        return None


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    for sensor_key, sensor_def in SENSOR_DEFINITIONS.items():
        value = get_value_from_path(coordinator.data or {}, sensor_def["path"])
        if value is not None:
            _LOGGER.debug("✅ Adding sensor '%s' from path: %s", sensor_key, sensor_def["path"])
            entities.append(PoolCopilotSensor(coordinator, sensor_key, sensor_def))
        else:
            _LOGGER.debug("⏭ Skipping sensor '%s' – key not in data or no data yet", sensor_key)

    async_add_entities(entities)
    _LOGGER.info("✅ All sensors added successfully")


class PoolCopilotSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, key, definition):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self.key = key
        self.definition = definition
        self._attr_name = definition["name"]
        self._attr_unique_id = f"{DOMAIN}_{key}"
        self._attr_native_unit_of_measurement = definition["unit"]

    @property
    def native_value(self):
        return get_value_from_path(self.coordinator.data or {}, self.definition["path"])

    @property
    def available(self):
        return self.coordinator.last_update_success and self.coordinator.data is not None

