import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.selector import NumberSelector, NumberSelectorConfig, NumberSelectorMode
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, CONF_SCAN_INTERVAL
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL

from dab_live_api import DAB

CONFIG_SCHEMA = vol.Schema({
    vol.Required(CONF_EMAIL): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})

class DABLiveFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for DAB Live!."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            valid = await self._test_credentials(
                user_input[CONF_EMAIL], user_input[CONF_PASSWORD]
            )
            if valid:
                return self.async_create_entry(
                    title=user_input[CONF_EMAIL], data=user_input
                )
            else:
                self._errors["base"] = "auth"

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input):
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=CONFIG_SCHEMA,
            errors=self._errors,
        )

    async def _test_credentials(self, email, password):
        """Return true if credentials is valid."""
        try:
            session = async_create_clientsession(self.hass)
            client = DAB(email, password, session, False)
            return await client.__authenticate__()
        except Exception:
            pass
        return False

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> config_entries.OptionsFlow:
        return DABLiveOptionsFlow(config_entry)


class DABLiveOptionsFlow(config_entries.OptionsFlow):
    """Handle DAB Live! options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options"""

        if user_input is not None:
            return self.async_create_entry(title='', data=user_input)
        
        options = self.config_entry.options
        scan_interval = options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

        return self.async_show_form(
            step_id='init',
            data_schema=vol.Schema({
                vol.Optional(CONF_SCAN_INTERVAL, default=scan_interval): cv.positive_int
            }), 
            last_step=True
        )