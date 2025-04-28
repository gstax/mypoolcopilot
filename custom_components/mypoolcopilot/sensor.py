from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTemperature

from .const import DOMAIN

class MyPoolCopilotSensor(SensorEntity):
    """Representation of a MyPoolCopilot sensor."""

    def __init__(self, coordinator, sensor_id, sensor_name, unit, device_class=None):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._attr_name = sensor_name
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_unique_id = sensor_id  # Only sensor_id
        self._attr_should_poll = False

    @property
    def available(self):
        """Return True if entity is available."""
        return self.coordinator.last_update_success

    @property
    def native_value(self):
        """Return the current value."""
        return self.coordinator.data.get(self._attr_unique_id)

    @property
    def device_info(self):
        """Return device information for grouping sensors."""
        return {
            "identifiers": {(DOMAIN, "mypoolcopilot_system")},
            "name": "MyPoolCopilot",
            "manufacturer": "MyPoolCopilot",
            "model": "PoolCopilot Integration",
            "entry_type": "service",
        }

    async def async_update(self):
        """Update the sensor."""
        await self.coordinator.async_request_refresh()

