from typing import Final
from enum import Enum
from homeassistant.components.switch import SwitchDeviceClass

DOMAIN: Final[str] = "dab_live!"
DOMAIN_DATA: Final[str] = "dab_live!_data"
ATTRIBUTION: Final[str] = "Data provided by DAB Live!"
VERSION: Final[str] = "0.0.1"

DEFAULT_NAME: Final[str] = DOMAIN
POWER_CONSUMPTION_ICON: Final[str] = "mdi:lightning-bolt"
WATER_CONSUMPTION_ICON: Final[str] = "mdi:water"

SENSOR: Final[str] = "sensor"
SWITCH: Final[str] = "switch"
PLATFORMS: Final[list[str]] = [SENSOR, SWITCH]

FLOW_COUNT: Final[str] = 'Actual_Period_Flow_Counter'
ENERGY_COUNT: Final[str] = 'Actual_Period_Energy_Counter'
POWER_SHOWER: Final[dict[str, str]] = {
    'name': 'Power shower',
    'platform': 'powershower',
    'icon': 'mdi:shower-head',
    'device_class': SwitchDeviceClass.SWITCH,
    'command_status': 'PowerShowerCommand',
    'command_on': 'ON',
    'command_off': 'OFF',
    'command_true_value': '1'
}

MODELS: Final[dict[str, str]] = {
    '108': 'EsyMini'
} 


DEFAULT_SCAN_INTERVAL = 60