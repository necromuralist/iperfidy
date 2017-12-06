"""Settings for the server"""
# from pypi
from voluptuous import (
    Schema,
    )
import voluptuous

# this project
from iperfidy.base import BaseSettings


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
            self._schema = Schema({})
        return self._schema
