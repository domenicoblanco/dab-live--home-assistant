from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import ATTRIBUTION, DOMAIN, MODELS

class DABLiveEntity(CoordinatorEntity):
    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator)
        self.config_entry = config_entry

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f'{self.zone['name']}_{self.platform_type}'

    @property
    def device_info(self):
        product_type = self.zone['pumps'][self.pump_id].get('ProductType')
        return {
            'hw_version': product_type,
            'identifiers': {(DOMAIN, self.zone['id'])},
            'name': self.zone['name'],
            'manufacturer': self.zone['company'],
            'model':  MODELS.get(product_type, product_type),
            'serial_number': self.zone['pumps'][self.pump_id].get('ProductSerialNumber'),
            'sw_version': self.zone['pumps'][self.pump_id].get('LvVersion')
        }

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            'attribution': ATTRIBUTION,
            'id': str(self.zone.get('id')),
            'integration': DOMAIN,
            'manufacturer': self.zone['company']
        }