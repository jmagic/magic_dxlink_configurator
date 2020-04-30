import datetime
import os
from dataclasses import dataclass, field
from shutil import which


class DXLinkUnit:

    def __init__(self, model='', hostname='', serial='', firmware='', device='', mac_address='',
                 ip_address='', arrival_time=datetime.datetime.now(), ip_type='', gateway='',
                 subnet='', master='', system='', status='', last_status=datetime.datetime.now()):

        self.model = model
        self.hostname = hostname
        self.serial = serial
        self.firmware = firmware
        self.device = device
        self.mac_address = mac_address
        self.ip_address = ip_address
        self.arrival_time = arrival_time
        self.ip_type = ip_type
        self.gateway = gateway
        self.subnet = subnet
        self.master = master
        self.system = system
        self.status = status
        self.last_status = last_status


@dataclass
class Preferences:
    master_address: str = '127.0.0.1'
    device_number: int = 0
    connection_type: str = 'TCP'
    device_dhcp: bool = True
    number_of_threads: int = 20
    telnet_client: str = None
    telnet_timeout: int = 20
    dhcp_listen: bool = True
    amx_only_filter: bool = False
    subnet_filter: str = ''
    subnet_filter_enable: bool = False
    play_sounds: bool = True
    randomize_sounds: bool = False
    check_for_updates: bool = True
    debug: bool = False
    dev_inc_num: int = 0
    cols_selected: list = field(default_factory=lambda: ['Time', 'Model', 'MAC', 'IP', 'Hostname', 'Serial',
                                                         'Firmware', 'Device', 'Static', 'Master', 'System', 'Status'])

    dxtx_models: list = field(default_factory=lambda: ['DXLINK-HDMI-MFTX', 'DXLINK-HDMI-WP', 'DXLINK-HDMI-DWP'])
    dxrx_models: list = field(default_factory=lambda: ['DXLINK-HDMI-RX', 'DXLINK-HDMI-RX.c', 'DXLINK-HDMI-RX.e'])
    dxftx_models: list = field(default_factory=lambda: ['DXF-TX-xxD', 'DXLF-MFTX'])
    dxfrx_models: list = field(default_factory=lambda: ['DXF-RX-xxD', 'DXLF-HDMIRX'])

    def set_prefs(self, storage_path):
        self.telnet_client = which('putty.exe')
        if self.telnet_client is None:
            # Check if we have a copy locally
            if os.path.exists(os.path.join(storage_path, 'putty.exe')):
                self.telnet_client = os.path.join(storage_path, 'putty.exe')
