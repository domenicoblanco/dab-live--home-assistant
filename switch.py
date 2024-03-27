from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN, POWER_SHOWER
from .entity import DABLiveEntity

async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    for zone in coordinator.data:
        for pump in zone.get('pumps'):
            entities.insert(0, DABLiveBinarySwitch(coordinator, entry, zone, pump, POWER_SHOWER))
    
    async_add_devices(entities)


class DABLiveBinarySwitch(DABLiveEntity, SwitchEntity):
    def __init__(self, coordinator, config_entry, zone, pump_id, switch_type):
        self.platform_type = switch_type['platform']
        self.zone = zone
        self.pump_id = pump_id
        self.switch_type = switch_type
        super().__init__(coordinator, config_entry)
    
    async def async_turn_on(self, **kwargs) -> None:
        """Turn on the switch."""
        await self.coordinator.api.handle_power_shower(self.switch_type['command_on'])
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn off the switch."""
        await self.coordinator.api.handle_power_shower(self.switch_type['command_off'])
        await self.coordinator.async_request_refresh()

    @property
    def name(self):
        """Return the name of the switch."""
        return self.switch_type['name']

    @property
    def icon(self):
        """Return the icon of this switch."""
        return self.switch_type['icon']

    @property
    def device_class(self):
        """Return de device class of the sensor."""
        return self.switch_type['device_class']

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self.zone['pumps'].get(self.switch_type['command_status']) == self.switch_type['command_true_value']