"""Settings for the server"""
# from pypi
from voluptuous import (
    Schema,
    )
import voluptuous

# this project
from iperfidy.base import BaseSettings


class ServerSettingsKeys:
    """Keys for the JSON requests

    attributes are iperf3-python names
    values are iperf3 options
    """
    bind_address = "bind"
    port = "port"
    verbose = "verbose"


class ServerSettingsAttributes:
    """the opposite of the ServerSettingsKeys"""
    bind = "bind_address"
    port = "port"
    verbose = "verbose"


class ServerSettings(BaseSettings):
    """Server Settings Validator

    Args:
     settings (dict): iperf settings for the server
    """
    @property
    def schema(self):
        """schema to validate the JSON

        Returns:
         :class:`voluptuous.Schema`: server settings validator
        """
        if self._schema is None:
            self._schema = Schema(
                {
                    ServerSettingsKeys.bind_address: str,
                    ServerSettingsKeys.port: int,
                    ServerSettingsKeys.verbose: bool,
                })
        return self._schema

    @property
    def settings_map(self):
        """Maps the iperf command-line options to the python attributes

        Returns:
         dict: map from iperf server options to Server object attributes
        """
        if self._settings_map is None:
            self._settings_map = {
                ServerSettingsKeys.bind_address: ServerSettingsAttributes.bind,
                ServerSettingsKeys.port: ServerSettingsAttributes.port,
                ServerSettingsKeys.verbose: ServerSettingsAttributes.verbose,
            }
        return self._settings_map


