from . import const
from .entity import DABLiveEntity
from homeassistant.const import UnitOfEnergy, UnitOfVolume
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass, SensorEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[const.DOMAIN][entry.entry_id]
    entities = []
    
    for zone in coordinator.data:
        for pump in zone.get('pumps'):
            entities.insert(0, DABLiveSensor(coordinator, entry, zone, pump, const.FLOW_COUNT))
            entities.insert(0, DABLiveSensor(coordinator, entry, zone, pump, const.ENERGY_COUNT))
    
    async_add_devices(entities)

class DABLiveSensor(DABLiveEntity, SensorEntity):
    """Sensor class."""
    def __init__(self, coordinator, config_entry, zone: dict, pump_id: str, sensor_type: str):
        self.zone = zone
        self.pump_id = pump_id
        self.type = sensor_type
        self.set_sensor_defaults(self.type)
        super().__init__(coordinator, config_entry)

    def set_sensor_defaults(self, sensor_type: str):
        match sensor_type:
            case const.FLOW_COUNT:
                self.__name = 'Water consumption'
                self.__icon = const.WATER_CONSUMPTION_ICON
                self.__device_class = SensorDeviceClass.WATER
                self.__unit_of_measurement = UnitOfVolume.CUBIC_METERS
                self.__state_class = SensorStateClass.TOTAL_INCREASING
                self.platform_type = SensorDeviceClass.WATER
            case const.ENERGY_COUNT:
                self.__name = 'Power consumption'
                self.__icon = const.POWER_CONSUMPTION_ICON
                self.__device_class = SensorDeviceClass.ENERGY
                self.__unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
                self.__state_class = SensorStateClass.TOTAL_INCREASING
                self.platform_type = SensorDeviceClass.POWER

    @property
    def name(self):
        """Return the name of the sensor."""
        return self.__name

    @property
    def state(self):
        """Return the state of the sensor."""
        data = self.zone['pumps'][self.pump_id].get(self.type)
        match self.type:
            case const.FLOW_COUNT:
                return f'{data[:-3]}.{data[-3:]}'
            case const.ENERGY_COUNT:
                return f'{data[:-1]}.{data[-1:]}'
    
    @property
    def native_value(self):
        """Return the native value of the sensor."""
        data = self.zone['pumps'][self.pump_id].get(self.type)
        match self.type:
            case const.FLOW_COUNT:
                return f'{data[:-3]}.{data[-3:]}'
            case const.ENERGY_COUNT:
                return f'{data[:-1]}.{data[-1:]}'

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self.__icon

    @property
    def device_class(self):
        """Return de device class of the sensor."""
        return self.__device_class

    @property
    def native_unit_of_measurement(self):
        """Return the native unit of measurement"""
        return self.__unit_of_measurement
    
    @property
    def unit_of_measurement(self):
        """Return the native unit of measurement"""
        return self.__unit_of_measurement

    @property
    def state_class(self):
        """Return the state class"""
        return self.__state_class
