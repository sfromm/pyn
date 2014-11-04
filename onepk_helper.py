#!/usr/bin/python

from onep.element.NetworkApplication import NetworkApplication
from onep.element import SessionConfig

ONEPK_PORT = 15002

class NetworkDevice(object):

    def __init__(self, ipaddr, username, password, pin_file=None, port=ONEPK_PORT):
        self.ipaddr = ipaddr
        self.username = username
        self.password = password
        self.pin_file = pin_file
        self.port = port

    def connect(self):
        ''' establish connection via onepk to network device '''
        self.network_application = NetworkApplication.get_instance()
        self.net_element = self.network_application.get_network_element(self.ipaddr)

        # create SessionConfig
        session_config = SessionConfig(SessionConfig.SessionTransportMode.TLS)
        session_config.ca_certs = None
        session_config.keyfile = None
        session_config.certfile = None
        session_config.port = self.port

        session_config.set_tls_pinning(self.pin_file, None)
        self.session_config = session_config

        self.session_handle = self.net_element.connect(self.username, self.password, self.session_config)

    def disconnect(self):
        ''' application will hang if you do not disconnect gracefully '''
        self.net_element.disconnect()
