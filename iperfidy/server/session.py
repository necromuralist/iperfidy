"""The Iperf Server Session"""
# from pypi
import iperf3

# this project
from iperfidy.base import IperfSession
from iperfidy.server.settings import ServerSettings


class ServerSession(IperfSession):
    """The Server Session"""
    @property
    def iperf_definition(self):
        """the Iperf definition

        Returns:
         :class:`iperf3.Server: server to run
        """
        return iperf3.Server

    @property
    def settings_definition(self):
        """the server settings class
        
        Returns:
         :class:`ServerSettings`: settings validator
        """
        return ServerSettings
