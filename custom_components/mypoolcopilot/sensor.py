import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SENSOR_MAPPING = {
    "orp": ("ORP", "mV"),
    "pH": ("pH", None),
    "temperature": ("Water Temperature", "°C", "PoolCop.temperature.water"),
    "air_temperature": ("Air Temperature", "°C", "PoolCop.temperature.air"),
    "pressure": ("Pressure", "bar", "PoolCop.pressure"),
    "voltage": ("Voltage", "V", "PoolCop.voltage"),
    "water_level": ("Water Level", None, "PoolCop.waterlevel"),
    "pump_status": ("Pump Status", None, "PoolCop.status.pump"),
    "pump_speed": ("Pump Speed", None, "PoolCop.status.pumpspeed"),
    "valve_position": ("Valve Position", None, "PoolCop.status.valveposition"),
    "ioniser_status": ("Ioniser Status", None, "PoolCop.status.ioniser"),
    "poolcop_status": ("PoolCop Status", None, "PoolCop.status.poolcop"),
}

def get_value_by_path(data, path):
    try:
        for key in path.split("."):
            data = data[key]
        return data
    except (KeyError, TypeError):
        return None

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    for key, (name, unit, *optional_path) in SENSOR_MAPPING.items():
        path = optional_path[0] if optional_path else f"PoolCop.{key}"
        value = get_value_by_path(coordinator.data, path)
        if value is not None:
            _LOGGER.debug("✅ Adding sensor '%s' from path: %s", key, path)
            entities.append(PoolCopilotSensor(coordinator, key, name, unit, path))
        else:
            _LOGGER.debug("Skipping sensor '%s' – key not in data or no data yet", key)

    async_add_entities(entities)
    _LOGGER.info("✅ All sensors added successfully")

class PoolCopilotSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, key, name, unit, path):
        super().__init__(coordinator)
        self._attr_name = f"PoolCopilot {name}"
        self._attr_unique_id = f"{DOMAIN}_{key}"
        self._attr_native_unit_of_measurement = unit
        self._path = path

    @property
    def native_value(self):
        return get_value_by_path(self.coordinator.data, self._path)

