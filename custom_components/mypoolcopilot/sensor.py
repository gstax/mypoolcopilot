"""Sensor platform for MyPoolCopilot integration."""

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.entity import EntityCategory
from dataclasses import dataclass

from .const import DOMAIN

@dataclass
class MyPoolCopilotSensorEntityDescription(SensorEntityDescription):
    """Describes a MyPoolCopilot sensor entity."""
    key: str
    translation_key: str

SENSOR_TYPES = [
    MyPoolCopilotSensorEntityDescription(
        key="temperature_water",
        translation_key="temperature_water",
        device_class="temperature",
    ),
    MyPoolCopilotSensorEntityDescription(
        key="temperature_air",
        translation_key="temperature_air",
        device_class="temperature",
    ),
    MyPoolCopilotSensorEntityDescription(
        key="pressure",
        translation_key="pressure",
    ),
    MyPoolCopilotSensorEntityDescription(
        key="pH",
        translation_key="pH",
    ),
    MyPoolCopilotSensorEntityDescription(
        key="orp",
        translation_key="orp",
    ),
    MyPoolCopilotSensorEntityDescription(
        key="ioniser",
        translation_key="ioniser",
    ),
    MyPoolCopilotSensorEntityDescription(
        key="voltage",
        translation_key="voltage",
        device_class="voltage",
    ),
    MyPoolCopilotSensorEntityDescription(
        key="waterlevel",
        translation_key="waterlevel",
    ),
    MyPoolCopilotSensorEntityDescription(
        key="status_pump",
        translation_key="status_pump",
    ),
    MyPoolCopilotSensorEntityDescription(
        key="status_pumpspeed",
        translation_key="status_pumpspeed",
    ),
    MyPoolCopilotSensorEntityDescription(
        key="status_valveposition",
        translation_key="status_valveposition",
    ),
    MyPoolCopilotSensorEntityDescription(
        key="status_poolcop",
        translation_key="status_poolcop",
    ),
]

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up MyPoolCopilot sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    for description in SENSOR_TYPES:
        entities.append(MyPoolCopilotSensor(coordinator, description))

    async_add_entities(entities)

class MyPoolCopilotSensor(SensorEntity):
    """Representation of a MyPoolCopilot sensor."""

    def __init__(self, coordinator, description: MyPoolCopilotSensorEntityDescription):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self.entity_description = description
        self._attr_unique_id = f"{DOMAIN}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, "mypoolcopilot")},
            "name": "MyPoolCopilot",
            "manufacturer": "PoolCopilot",
        }

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self.entity_description.key)

