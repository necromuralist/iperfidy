"""Some Base Classes"""

# python standard library
from abc import (
    abstractproperty,
    ABC,
    )
import logging
from logging.handlers import RotatingFileHandler
import os

# pypi
from voluptuous import humanize
import voluptuous

LEVELS = {"DEBUG": logging.DEBUG,
          "INFO": logging.INFO,
          "WARNING": logging.WARNING}
LOG_FORMAT = ("%(asctime)s : %(levelname)s: %(filename)s :"              
              " %(name)s (line %(lineno)d) : %(message)s")
LOG_LEVEL = LEVELS[os.environ.get("LOG_LEVEL", "INFO")]
SCREEN_FORMAT = "%(levelname)s: %(message)s"
LOG_PATH = "/tmp/iperfidy.log"


class InvalidSettings(Exception):
    """Exception for bad server-settings"""


class BaseSettings(ABC):
    """something with logging
    
    Args:
     settings (dict): the settings to validate
    """
    def __init__(self, settings, log_path=LOG_PATH):
        self.settings = settings
        self.log_path = log_path
        self._schema = None
        self._log = None
        return

    @property
    def log(self):
        """console log

        Returns:
         :class:`logging.Logger`: python logger for the console
        """
        if self._log is None:
            self._log = logging.getLogger(self.__class__.__name__)
            self._log.setLevel(LOG_LEVEL)
            formatter = logging.Formatter(SCREEN_FORMAT)
            handler = logging.StreamHandler()
            handler.setLevel(LOG_LEVEL)
            handler.setFormatter(formatter)
            self._log.addHandler(handler)
            formatter = logging.Formatter(LOG_FORMAT)
            handler = RotatingFileHandler(self.log_path)
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(formatter)
            self._log.addHandler
        return self._log    

    @abstractproperty
    def schema(self):
        """Schema to validate the settings"""
        return

    def validate(self):
        """validates the JSON

        Raises:
         InvalidServerSettings: bad entry in the JSON
        """
        try:
            humanize.validate_with_humanized_errors(self.settings, self.schema)
        except voluptuous.Error as error:
            self.log.error(error)
            raise InvalidSettings("bad settings {}".format(error))
        return
    
