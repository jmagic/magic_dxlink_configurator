"""Configurator is a program that integrates device discovery and telnet 
commands to ease configuration and management of AMX DXLink devices.

The MIT License (MIT)

Copyright (c) 2014 Jim Maciejewski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""


import ConfigParser
import wx
import pickle
import datetime
import os
import csv
from ObjectListView import ObjectListView, ColumnDefn
import Queue
import webbrowser
import requests
import urllib
from bs4 import BeautifulSoup
from distutils.version import StrictVersion
from pydispatch import dispatcher
from threading import Thread
import subprocess
import sys

from scripts import (config_menus, dhcp_sniffer, mdc_gui, send_command,
                     multi_ping, mse_baseline, telnet_class, telnetto_class,
                     dipswitch)


class Unit(object):
    """
    Model of the Unit

    Contains the following attributes:
    model, hostname, serial ,firmware, device, mac, ip, time, ip_type, gateway,
    subnet, master, system
    """
    # ----------------------------------------------------------------------
    def __init__(self,  model='', hostname='', serial='', firmware='',
                 device='', mac='', ip_ad='', arrival_time='', ip_type='',
                 gateway='', subnet='', master='', system='', status=''):

        self.model = model
        self.hostname = hostname
        self.serial = serial
        self.firmware = firmware
        self.device = device
        self.mac_address = mac
        self.ip_address = ip_ad
        self.arrival_time = arrival_time
        self.ip_type = ip_type
        self.gateway = gateway
        self.subnet = subnet
        self.master = master
        self.system = system
        self.status = status


class MainFrame(mdc_gui.MainFrame):
    def __init__(self, parent):
        mdc_gui.MainFrame.__init__(self, parent)

        self.parent = parent
        self.name = "Magic DXLink Configurator"
        self.version = "v3.1.0"

        icon_bundle = wx.IconBundle()
        icon_bundle.AddIconFromFile(r"icon\\MDC_icon.ico", wx.BITMAP_TYPE_ANY)
        self.SetIcons(icon_bundle)

        self.dxtx_models_default = (
            'DXLINK-HDMI-MFTX, ' +
            'DXLINK-HDMI-WP, ' +
            'DXLINK-HDMI-DWP')

        self.dxrx_models_default = (
            'DXLINK-HDMI-RX, ' +
            'DXLINK-HDMI-RX.c, ' +
            'DXLINK-HDMI-RX.e')
        self.dxftx_models_default = (
            'DXF-TX-xxD, ' +
            'DXLF-MFTX')
        self.dxfrx_models_default = (
            'DXF-RX-xxD, ' +
            'DXLF-HDMIRX')
        self.columns_default = (
            'Model, ' +
            'Hostname, ' +
            'Firmware, ' +
            'Static, ' +
            'MAC, ' +
            'Serial, ' +
            'Device, ' +
            'Master, ' +
            'System')

        self.master_address = None
        self.device_number = None
        self.default_connection_type = None
        self.default_dhcp = None
        self.thread_number = None
        self.telnet_client = None
        self.telnet_timeout_seconds = None
        self.dhcp_sniffing = None
        self.amx_only_filter = None
        self.play_sounds = None
        self.check_for_updates = None
        self.columns_config = []
        self.dxtx_models = []
        self.dxrx_models = []
        self.dxftx_models = []
        self.dxfrx_models = []
        self.config_fail = False
        self.telnet_missing = False
        self.path = os.path.expanduser(
                '~\\Documents\\Magic_DXLink_Configurator\\')
        self.read_config_file()
        self.check_for_telnet_client()

        self.set_title_bar()

        self.errorlist = []
        self.completionlist = []
        self.configure_list = []
        self.mse_active_list = []
        self.serial_active = []
        self.port_error = False
        self.ping_objects = []
        self.ping_active = False
        self.ping_window = None
        self.abort = False
        self.dev_inc_num = 0

        self.main_list = ObjectListView(self.olv_panel, wx.ID_ANY,
                                        style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.main_list.cellEditMode = ObjectListView.CELLEDIT_DOUBLECLICK
        self.main_list.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,
                            self.MainFrameOnContextMenu)
        self.main_list.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

        self.columns = []
        self.min_panel_width = 450
        self.panel_width_offset = 60
        self.col_width = {
                            'Time': 110,
                            'Model': 160,
                            'MAC': 125,
                            'IP': 120,
                            'Hostname': 150,
                            'Serial': 150,
                            'Firmware': 80,
                            'Device': 80,
                            'Static': 50,
                            'Master': 120,
                            'System': 60,
                            'Status': 120}

        self.columns_setup = [
            ColumnDefn("Time", "center", self.col_width['Time'],
                       "arrival_time", stringConverter="%I:%M:%S%p"),
            ColumnDefn("Model", "left", self.col_width['Model'], "model"),
            ColumnDefn("MAC", "left", self.col_width['MAC'], "mac_address"),
            ColumnDefn("IP", "left", self.col_width['IP'], "ip_address"),
            ColumnDefn("Hostname", "left", self.col_width['Hostname'],
                       "hostname"),
            ColumnDefn("Serial", "left", self.col_width['Serial'], "serial"),
            ColumnDefn("Firmware", "left", self.col_width['Firmware'],
                       "firmware"),
            ColumnDefn("Device", "left", self.col_width['Device'], "device"),
            ColumnDefn("Static", "left", self.col_width['Static'], "ip_type"),
            ColumnDefn("Master", "left", self.col_width['Master'], "master"),
            ColumnDefn("System", "left", self.col_width['System'], "system"),
            ColumnDefn("Status", "left", self.col_width['Status'], "status")]

        self.select_columns()
        self.amx_only_filter_chk.Check(self.amx_only_filter)
        self.dhcp_sniffing_chk.Check(self.dhcp_sniffing)
        self.load_data_pickle()
        self.update_status_bar()

        self.olv_sizer.Add(self.main_list, 1, wx.ALL | wx.EXPAND, 0)
        self.olv_sizer.Layout()
        self.resize_frame()
        self.cert_path = self.resource_path('cacert.pem')

        # Create DHCP listening thread
        self.dhcp_listener = dhcp_sniffer.DHCPListener(self)
        self.dhcp_listener.setDaemon(True)
        self.dhcp_listener.start()

        # create a telenetto thread pool and assign them to a queue
        self.telnet_to_queue = Queue.Queue()
        for _ in range(10):
            self.telnet_to_thread = telnetto_class.TelnetToThread(
                self, self.telnet_to_queue)
            self.telnet_to_thread.setDaemon(True)
            self.telnet_to_thread.start()

        # create a telnetjob thread pool and assign them to a queue
        self.telnet_job_queue = Queue.Queue()
        for _ in range(int(self.thread_number)):
            self.telnet_job_thread = telnet_class.Telnetjobs(
                self, self.telnet_job_queue)
            self.telnet_job_thread.setDaemon(True)
            self.telnet_job_thread.start()

        dispatcher.connect(self.incoming_packet,
                           signal="Incoming Packet",
                           sender=dispatcher.Any)
        dispatcher.connect(self.set_status,
                           signal="Status Update",
                           sender=dispatcher.Any)
        dispatcher.connect(self.collect_completions,
                           signal="Collect Completions",
                           sender=dispatcher.Any)
        dispatcher.connect(self.collect_errors,
                           signal="Collect Errors",
                           sender=dispatcher.Any)
        self.dhcp_listener.dhcp_sniffing_enabled = self.dhcp_sniffing

        if self.check_for_updates:
            Thread(target=self.update_check).start()

    # ----------------------------------------------------------------------

    def resource_path(self, relative):
        return os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(".")),
                            relative)

    def update_check(self):
        """Checks on line for updates"""
        # print 'in update'
        try:
            webpage = requests.get(
              'https://github.com/AMXAUNZ/Magic-DXLink-Configurator/releases',
              verify=self.cert_path)
            # Scrape page for latest version
            soup = BeautifulSoup(webpage.text)
            # Get the <div> sections in lable-latest
            # print 'divs'
            divs = soup.find_all("div", class_="release label-latest")
            # Get the 'href' of the release
            url_path = divs[0].find_all('a')[-3].get('href')
            # Get the 'verison' number
            online_version = url_path.split('/')[-2][1:]
            if StrictVersion(online_version) > StrictVersion(self.version[1:]):
                # Try update
                # print 'try update'
                self.do_update(url_path, online_version)
            else:
                # All up to date pass
                # print 'up to date'
                return
        except Exception as error:
            # print 'error'error
            # we have had a problem, maybe update will work next time.
            # print 'error ', error
            pass

    def do_update(self, url_path, online_version):
        """download and install"""
        # ask if they want to update
        dlg = wx.MessageDialog(
                parent=self,
                message='A new Magic DXLink Configurator is available v' +
                        str(StrictVersion(online_version)) + '\r' +
                        'Do you want to download and update?',
                        caption='Do you want to update?',
                        style=wx.OK | wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            response = requests.get('https://github.com' + url_path,
                                    verify=self.cert_path, stream=True)
            if not response.ok:
                return
            total_length = response.headers.get('content-length')
            if total_length is None:  # no content length header
                pass
            else:
                total_length = int(total_length) / 1024
            dlg = wx.ProgressDialog("Progress dialog example",
                                    "An informative message",
                                    maximum=total_length,
                                    parent=self,
                                    style=wx.PD_APP_MODAL
                                    | wx.PD_AUTO_HIDE
                                    | wx.PD_CAN_ABORT
                                    | wx.PD_ESTIMATED_TIME
                                    | wx.PD_REMAINING_TIME
                                    | wx.PD_SMOOTH
                                    )
            temp_folder = os.environ.get('temp')
            with open(temp_folder +
                      'Magic_DXLink_Configurator_Setup_' +
                      str(StrictVersion(online_version)), 'wb') as handle:

                count = 0
                for data in response.iter_content(1024):
                    count += len(data) / 1024
                    handle.write(data)
                    (cancel, skip) = dlg.Update(count - 1)
                    if not cancel:
                        print 'cancel pressed'
                        break
                        
                print 'out of for loop'
            dlg.Destroy()
            self.install_update()

    def install_update(self):
        """Installs the downloaded update"""
            #if not abort:
            #    return  # since we aborted the download, don't try to install
            # close program & launch installer
            # print 'downloaded'

        dlg = wx.MessageDialog(
            parent=self,
            message='Do you want to update to version ' +
                    str(StrictVersion(online_version)) + ' now?',
            caption='Update program',
            style=wx.OK | wx.CANCEL)

        if dlg.ShowModal() == wx.ID_OK:
            subprocess.Popen(temp_folder +
                             'Magic_DXLink_Configurator_Setup_' +
                             str(StrictVersion(online_version)))
            self.on_close(None)

    def on_key_down(self, event):
        """Grab Delete key presses"""
        key = event.GetKeyCode()
        if key == wx.WXK_DELETE:
            dlg = wx.MessageDialog(
                parent=self,
                message='Are you sure? \n\nThis will delete all selected' +
                ' items in the list',
                caption='Delete All Selected Items',
                style=wx.OK | wx.CANCEL)

            if dlg.ShowModal() == wx.ID_OK:
                self.delete_item(None)
                self.dump_pickle()
            else:
                return
        event.Skip()

    def play_sound(self):
        """Plays a barking sound"""
        if self.play_sounds:
            filename = "sounds\\woof.wav"
            sound = wx.Sound(filename)
            if sound.IsOk():
                sound.Play(wx.SOUND_ASYNC)
            else:
                wx.MessageBox("Invalid sound file", "Error")

    def set_status(self, sender):
        """sets the status of an object from a tuple of (obj, status)"""
        sender[0].status = sender[1]
        self.main_list.RefreshObject(sender[0])

    def communication_started(self, sender):
        """Updates status when communication is started"""
        sender.status = "Connecting"
        self.main_list.RefreshObject(sender)

    def collect_completions(self, sender):
        """Creates a list of completed connections"""
        self.completionlist.append(sender)
        sender.status = "Success"
        self.main_list.RefreshObject(sender)

    def collect_errors(self, sender):
        """Creates a list of incomplete connections"""
        self.errorlist.append(sender)
        sender[0].status = "Failed: " + sender[1]
        self.main_list.RefreshObject(sender[0])

    def port_errors(self):
        """Shows when the listening port is in use"""
        dlg = wx.MessageDialog(
            self,
            message='Unable to use port 67\n No DHCP requests will be added.',
            caption='Port in use',
            style=wx.ICON_INFORMATION)
        dlg.ShowModal()
        self.dhcp_sniffing_chk.Enable(False)
        self.amx_only_filter_chk.Enable(False)

    def on_dhcp_sniffing(self, _):
        """Turns sniffing on and off"""
        self.dhcp_sniffing = not self.dhcp_sniffing
        self.dhcp_sniffing_chk.Check(self.dhcp_sniffing)
        self.dhcp_listener.dhcp_sniffing_enabled = self.dhcp_sniffing
        self.write_config_file()

    def on_amx_only_filter(self, _):
        """Turns amx filtering on and off"""
        self.amx_only_filter = not self.amx_only_filter
        self.amx_only_filter_chk.Check(self.amx_only_filter)
        self.write_config_file()

    def select_columns(self):
        """Sets the columns to be displayed"""
        # assert isinstance(self.columns_config, basestring)
        columns = self.columns_config + ['Time', 'IP', 'Status']
        todisplay = []
        for item in self.columns_setup:
            if item.title in columns:
                todisplay.append(item)
        self.main_list.SetColumns(todisplay)

    def check_for_none_selected(self):
        """Checks if nothing is selected"""
        if len(self.main_list.GetSelectedObjects()) == 0:
            dlg = wx.MessageDialog(
                parent=self, message='Nothing selected...\nPlease click on ' +
                'the device you want to select',
                caption='Nothing Selected',
                style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return True
        for obj in self.main_list.GetSelectedObjects():
            self.set_status((obj, ''))

    def on_select_all(self, _):
        """Select all items in the list"""
        self.main_list.SelectAll()

    def on_select_none(self, _):
        """Select none of the items in the list"""
        self.main_list.DeselectAll()

    def config_fail_dia(self):
        """show config fail"""
        dlg = wx.MessageDialog(
            parent=self,
            message='New setting file created \n\n I\'ve had to create a new' +
            ' settings file, \nbecause the old one couldn\'t be read \n' +
            'or was from a old version',
            caption='Default settings file created',
            style=wx.OK)

        dlg.ShowModal()

    def telnet_to(self, _):
        """Telnet to the selected device(s)"""
        if self.check_for_none_selected():
            return
        if len(self.main_list.GetSelectedObjects()) > 10:
            dlg = wx.MessageDialog(
                parent=self,
                message='I can only telnet to 10 devices at a time \nPlease ' +
                'select less than ten devices at once',
                caption='How many telnets?',
                style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return

        if os.path.exists((self.path + self.telnet_client)):

            for obj in self.main_list.GetSelectedObjects():
                self.telnet_to_queue.put([obj, 'telnet'])
                self.set_status((obj, "Queued"))
        else:
            dlg = wx.MessageDialog(
                parent=self, message='Could not find ' +
                'telnet client \nPlease put ' +
                '%s in \n%s' % (self.telnet_client, self.path),
                caption='No %s' % self.telnet_client,
                style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()

    def ssh_to(self, _):
        """Telnet to the selected device(s)"""
        if self.check_for_none_selected():
            return
        if len(self.main_list.GetSelectedObjects()) > 10:
            dlg = wx.MessageDialog(
                parent=self, message='I can only ssh to' +
                ' 10 devices at a time \nPlease select less' +
                ' than ten devices at once',
                caption='How many ssh?',
                style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return
        if os.path.exists((self.path + self.telnet_client)):

            for obj in self.main_list.GetSelectedObjects():
                self.telnet_to_queue.put([obj, 'ssh'])
                self.set_status((obj, "Queued"))
        else:
            dlg = wx.MessageDialog(
                parent=self,
                message='Could not find telnet client \nPlease put ' +
                '%s in \n%s' % (self.telnet_client, self.path),
                caption='No %s' % self.telnet_client,
                style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        return

    def mse_baseline(self, _):
        """Shows the MSE baseline"""
        if self.check_for_none_selected():
            return
        if len(self.main_list.GetSelectedObjects()) > 10:
            dlg = wx.MessageDialog(
                parent=self,
                message='I can only telnet to 10 devices at a time \nPlease ' +
                'select less than ten devices at once',
                caption='How many telnets?',
                style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return
        for obj in self.main_list.GetSelectedObjects():
            if self.mse_rx_check(obj):
                if not self.mse_in_active(obj):
                    self.mse_enable_thread(obj)
                self.mse_active_list.append(obj.mac_address)
                dia = mse_baseline.MSE_Baseline(self, obj)
                dia.Show()

    def mse_enable_thread(self, obj):
        """Adds mse thread for plotting / baseline"""
        self.telnet_job_queue.put(['get_dxlink_mse', obj,
                                   self.telnet_timeout_seconds])
        self.set_status((obj, "Queued"))

    def mse_in_active(self, obj):
        """Checks if device is in active list"""
        if obj.mac_address in self.mse_active_list:
            dlg = wx.MessageDialog(parent=self, message='You are already ' +
                                   'getting MSE from this MAC address',
                                   caption='Are you sure?',
                                   style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return True
        return False

    def mse_rx_check(self, obj):
        """Checks if device is a RX"""
        if obj.model not in self.dxrx_models:
            dlg = wx.MessageDialog(parent=self, message='This does not ' +
                                   'appear to be a RX device. You can only' +
                                   ' get MSE values from RX devices. Click ' +
                                   'OK to continue anyway.',
                                   caption='MSE only works on RX devices',
                                   style=wx.O | wx.CANCEL)
            if dlg.ShowModal() != wx.ID_OK:
                dlg.Destroy()
                return False
            dlg.Destroy()
        return True

    def on_dipswitch(self, _):
        """View what the dipswitches do"""
        dia = dipswitch.ShowDipSwitch(self)
        dia.Show()

    def multi_ping(self, _):
        """Ping and track results of many devices"""
        if self.check_for_none_selected():
            return
        if self.ping_active:
            dlg = wx.MessageDialog(parent=self, message='You already have a ' +
                                   'ping window open',
                                   caption='Are you crazy?',
                                   style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return
        if len(self.main_list.GetSelectedObjects()) > int(self.thread_number):
            dlg = wx.MessageDialog(parent=self, message='I can only ping ' +
                                   self.thread_number +
                                   ' devices at a time \nPlease select less ' +
                                   'than ' + self.thread_number +
                                   ' devices at once',
                                   caption='How many pings?',
                                   style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return

        self.ping_active = True
        self.ping_window = multi_ping.MultiPing(
            self, self.main_list.GetSelectedObjects())
        self.ping_window.Show()

    def factory_av(self, _):
        """Reset device AV settings to factory defaults"""
        if self.check_for_none_selected():
            return

        for obj in self.main_list.GetSelectedObjects():
            self.telnet_job_queue.put(['factory_av', obj,
                                       self.telnet_timeout_seconds])
            self.set_status((obj, "Queued"))

    def reset_factory(self, _):
        """Reset device to factory defaults"""
        if self.check_for_none_selected():
            return
        for obj in self.main_list.GetSelectedObjects():
            dlg = wx.MessageDialog(parent=self, message='Are you sure? \n ' +
                                   'This will reset %s' % obj.ip_address,
                                   caption='Factory Reset',
                                   style=wx.OK | wx.CANCEL)
            if dlg.ShowModal() == wx.ID_OK:
                dlg.Destroy()
                self.telnet_job_queue.put(['reset_factory', obj,
                                           self.telnet_timeout_seconds])
                self.set_status((obj, "Queued"))

            else:
                return

    def reboot(self, _):
        """Reboots device"""
        if self.check_for_none_selected():
            return
        for obj in self.main_list.GetSelectedObjects():
            self.telnet_job_queue.put(['reboot', obj,
                                       self.telnet_timeout_seconds])
            self.set_status((obj, "Queued"))

    def open_url(self, _):
        """Opens ip address in a browser"""
        if self.check_for_none_selected():
            return
        for obj in self.main_list.GetSelectedObjects():
            url = 'http://' + obj.ip_address
            webbrowser.open_new_tab(url)

    def update_device_information(self, _):
        """Connects to device via telnet and gets serial model and firmware """
        if self.check_for_none_selected():
            return
        for obj in self.main_list.GetSelectedObjects():
            self.telnet_job_queue.put(['get_config_info', obj,
                                       self.telnet_timeout_seconds])
            self.set_status((obj, "Queued"))

    def turn_on_leds(self, _):
        """Turns on front panel LEDs"""
        if self.check_for_none_selected():
            return
        for obj in self.main_list.GetSelectedObjects():
            self.telnet_job_queue.put(['turn_on_leds', obj,
                                       self.telnet_timeout_seconds])
            self.set_status((obj, "Queued"))

    def turn_off_leds(self, _):
        """Turns off front panel LEDs"""
        if self.check_for_none_selected():
            return
        for obj in self.main_list.GetSelectedObjects():
            self.telnet_job_queue.put(['turn_off_leds', obj,
                                       self.telnet_timeout_seconds])
            self.set_status((obj, "Queued"))

    def enable_wd(self, _):
        """Enables the Watchdog"""
        if self.check_for_none_selected():
            return
        for obj in self.main_list.GetSelectedObjects():
            self.telnet_job_queue.put(['set_watchdog', obj,
                                       self.telnet_timeout_seconds, True])
            self.set_status((obj, "Queued"))

    def disable_wd(self, _):
        """disables the Watchdog"""
        if self.check_for_none_selected():
            return
        for obj in self.main_list.GetSelectedObjects():
            self.telnet_job_queue.put(['set_watchdog', obj,
                                       self.telnet_timeout_seconds, False])
            self.set_status((obj, "Queued"))

    def send_commands(self, _):
        """Send commands to selected devices"""
        if self.check_for_none_selected():
            return
        dxtx_devices = []
        dxrx_devices = []
        dxftx_devices = []
        dxfrx_devices = []
        for obj in self.main_list.GetSelectedObjects():
            if obj.model in self.dxtx_models:
                dxtx_devices.append(obj)
            elif obj.model in self.dxrx_models:
                dxrx_devices.append(obj)
            elif obj.model in self.dxftx_models:
                dxftx_devices.append(obj)
            elif obj.model in self.dxfrx_models:
                dxfrx_devices.append(obj)
            else:
                pass
        if len(dxtx_devices) != 0:
            dia_tx = send_command.SendCommandConfig(
                self, dxtx_devices, 'dxtx')
            dia_tx.Show()

        if len(dxrx_devices) != 0:
            dia_rx = send_command.SendCommandConfig(
                self, dxrx_devices, 'dxrx')
            dia_rx.Show()
        if len(dxftx_devices) != 0:
            dia_ftx = send_command.SendCommandConfig(
                self, dxftx_devices, 'dxftx')
            dia_ftx.Show()

        if len(dxfrx_devices) != 0:
            dia_frx = send_command.SendCommandConfig(
                self, dxfrx_devices, 'dxfrx')
            dia_frx.Show()

        if (len(dxtx_devices) + len(dxrx_devices) +
                len(dxftx_devices) + len(dxfrx_devices)) == 0:
            dlg = wx.MessageDialog(parent=self, message='No DXLink Devices ' +
                                   'Selected',
                                   caption='Cannot send commands',
                                   style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()

        self.errorlist = []
        self.completionlist = []

    def dump_pickle(self):
        """Saves list data to a file"""
        pickle.dump(self.main_list.GetObjects(), open(
            (self.path + 'data_' + self.version + '.pkl'), 'wb'))

    def export_to_csv(self, _):
        """Store list items in a CSV file"""
        if self.check_for_none_selected():
            return
        save_file_dialog = wx.FileDialog(
            self,
            message='Select file to add devices to or create a new file',
            defaultDir=self.path,
            defaultFile="",
            wildcard="CSV files (*.csv)|*.csv",
            style=wx.SAVE)
        if save_file_dialog.ShowModal() == wx.ID_OK:
            path = save_file_dialog.GetPath()
            with open(path, 'ab') as store_file:
                write_csv = csv.writer(store_file, quoting=csv.QUOTE_ALL)
                for obj in self.main_list.GetSelectedObjects():
                    data = [obj.model,
                            obj.hostname,
                            obj.serial,
                            obj.firmware,
                            obj.device,
                            obj.mac_address,
                            obj.ip_address,
                            obj.arrival_time,
                            obj.ip_type,
                            obj.gateway,
                            obj.subnet,
                            obj.master,
                            obj.system]

                    write_csv.writerow(data)
                    self.set_status((obj, 'Exported'))
            self.dump_pickle()

    def import_csv_file(self, _):
        """Imports a list of devices to the main list"""
        open_file_dialog = wx.FileDialog(self, message="Import a CSV file",
                                         defaultDir=self.path,
                                         defaultFile="",
                                         wildcard="CSV files (*.csv)|*.csv",
                                         style=wx.FD_OPEN
                                         | wx.FD_FILE_MUST_EXIST)
        if open_file_dialog.ShowModal() == wx.ID_OK:
            open_file_dialog.Destroy()
            dlg = wx.MessageDialog(parent=self, message='To replace ' +
                                   'all items currently in your list,  ' +
                                   'click ok',
                                   caption='Replace items',
                                   style=wx.OK | wx.CANCEL)
            if dlg.ShowModal() == wx.ID_OK:
                self.main_list.DeleteAllItems()

            with open(open_file_dialog.GetPath(), 'rb') as csvfile:
                cvs_data = csv.reader(csvfile)
                for item in cvs_data:
                    data = Unit(
                        model=item[0],
                        hostname=item[1],
                        serial=item[2],
                        firmware=item[3],
                        device=item[4],
                        mac=item[5],
                        ip_ad=item[6],
                        arrival_time=datetime.datetime.strptime(
                            (item[7]), "%Y-%m-%d %H:%M:%S.%f"),
                        ip_type=item[8],
                        gateway=item[9],
                        subnet=item[10],
                        master=item[11],
                        system=item[12])

                    self.main_list.AddObject(data)
            self.dump_pickle()

        else:
            open_file_dialog.Destroy()

    def import_ip_list(self, _):
        """Imports a list of IP addresses"""
        open_file_dialog = wx.FileDialog(
            self, message="Open IP List",
            defaultDir=self.path,
            defaultFile="",
            wildcard="CSV files (*.csv)|*.csv",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if open_file_dialog.ShowModal() == wx.ID_OK:
            self.main_list.DeleteAllItems()
            with open(open_file_dialog.GetPath(), 'rb') as csvfile:
                cvs_data = csv.reader(csvfile)
                for item in cvs_data:
                    data = Unit(
                        ip_ad=item[0],
                        arrival_time=datetime.datetime.now())

                    self.main_list.AddObject(data)
            self.dump_pickle()
            open_file_dialog.Destroy()
        else:
            open_file_dialog.Destroy()

    def generate_list(self, _):
        """Generates a list of ip addresses"""
        dia = config_menus.IpListGen(self)
        dia.ShowModal()
        dia.Destroy()

    def add_line(self, _):
        """Adds a line to the main list"""
        data = Unit(arrival_time=datetime.datetime.now())
        self.main_list.AddObject(data)
        self.dump_pickle()

    def delete_item(self, _):
        """Deletes the selected item"""
        if len(self.main_list.GetSelectedObjects()) == \
           len(self.main_list.GetObjects()):
            self.main_list.DeleteAllItems()
            self.dump_pickle()
            return
        if len(self.main_list.GetSelectedObjects()) == 0:
            return
        self.main_list.RemoveObjects(self.main_list.GetSelectedObjects())
        self.dump_pickle()

    def delete_all_items(self, _):
        """Deletes all items,selected or not"""
        dlg = wx.MessageDialog(parent=self, message='Are you sure? \n This ' +
                               'will delete all items in the list',
                               caption='Delete All Items',
                               style=wx.OK | wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            self.main_list.DeleteAllItems()
            self.dump_pickle()
        else:
            return

    def create_add_unit(self, model='', hostname='', serial='', firmware='',
                        device='', mac='', ip_ad='', arrival_time='',
                        ip_type='', gateway='', subnet='', master='',
                        system=''):
        """Creates and adds a unit"""
        data = Unit(
            model=model,
            hostname=hostname,
            serial=serial,
            firmware=firmware,
            device=device,
            mac=mac,
            ip_ad=ip_ad,
            arrival_time=datetime.datetime.now(),
            ip_type=ip_type,
            gateway=gateway,
            subnet=subnet,
            master=master,
            system=system)
        self.main_list.AddObject(data)
        # self.dump_pickle()
        return data

    def incoming_packet(self, sender):
        """Receives dhcp requests and adds them to objects to display"""
        incoming_time = datetime.datetime.now()
        data = Unit(
            hostname=sender[0],
            mac=sender[1],
            ip_ad=sender[2],
            arrival_time=incoming_time)

        self.status_bar.SetStatusText(
            incoming_time.strftime('%I:%M:%S%p') +
            ' -- ' + data.hostname +
            ' ' + data.ip_address +
            ' ' + data.mac_address)

        if bool(self.amx_only_filter):
            if data.mac_address[0:8] != '00:60:9f':
                self.main_list.SetFocus()
                return
        selected_items = self.main_list.GetSelectedObjects()
        if self.main_list.GetObjects() == []:
            self.main_list.AddObject(data)
            self.set_status((data, "DHCP"))
        else:
            for obj in self.main_list.GetObjects():
                if obj.mac_address == data.mac_address:
                    time_between_packets = (incoming_time -
                                            datetime.timedelta(seconds=2))
                    if obj.arrival_time > time_between_packets:
                        break
                    data.model = obj.model
                    data.serial = obj.serial
                    data.firmware = obj.firmware
                    data.device = obj.device
                    data.ip_type = obj.ip_type
                    data.gateway = obj.gateway
                    data.subnet = obj.subnet
                    data.master = obj.master
                    data.system = obj.system
                    if obj in selected_items:
                        selected_items.append(data)
                    self.main_list.RemoveObject(obj)
            self.main_list.AddObject(data)

            self.set_status((data, "DHCP"))
        if data.hostname[:2] == 'DX':
            self.telnet_job_queue.put(['get_config_info', data,
                                       self.telnet_timeout_seconds])
        self.main_list.SelectObjects(selected_items, deselectOthers=True)
        self.dump_pickle()
        self.play_sound()

    def read_config_file(self):
        """Reads the config file"""
        config = ConfigParser.RawConfigParser()
        try:  # read the settings file
            config.read((self.path + "settings.txt"))
            self.master_address = (config.get(
                'Settings', 'default master address'))
            self.device_number = (config.get(
                'Settings', 'default device number'))
            self.default_connection_type = (config.get(
                'Settings', 'default connection type'))
            self.default_dhcp = (config.getboolean(
                'Settings', 'default enable DHCP'))
            self.thread_number = (config.get(
                'Settings', 'number of threads'))
            self.telnet_client = (config.get(
                'Settings', 'telnet client executable'))
            self.telnet_timeout_seconds = (config.get(
                'Settings', 'telnet timeout in seconds'))
            self.dhcp_sniffing = (config.getboolean(
                'Settings', 'DHCP sniffing enabled'))
            self.amx_only_filter = (config.getboolean(
                'Settings', 'filter incoming DHCP for AMX only'))
            self.play_sounds = (config.getboolean(
                'Settings', 'play sounds'))
            self.check_for_updates = (config.getboolean(
                'Settings', 'check for updates'))
            self.columns_config = []
            for item in config.get(
                    'Config', 'columns_config').split(','):
                self.columns_config.append(item.strip())

            for item in config.get(
                    'Config', 'DXLink TX Models').split(','):
                self.dxtx_models.append(item.strip())
                for item in self.dxtx_models_default.split(','):
                    if item.strip() not in self.dxtx_models:
                        self.dxtx_models.append(item.strip())
            for item in config.get(
                    'Config', 'DXLink RX Models').split(','):
                self.dxrx_models.append(item.strip())
                for item in self.dxrx_models_default.split(','):
                    if item.strip() not in self.dxrx_models:
                        self.dxrx_models.append(item.strip())
            for item in config.get(
                    'Config', 'DXLink Fibre TX Models').split(','):
                self.dxftx_models.append(item.strip())
                for item in self.dxftx_models_default.split(','):
                    if item.strip() not in self.dxftx_models:
                        self.dxftx_models.append(item.strip())
            for item in config.get(
                    'Config', 'DXLink Fibre RX Models').split(','):
                self.dxfrx_models.append(item.strip())
                for item in self.dxfrx_models_default.split(','):
                    if item.strip() not in self.dxfrx_models:
                        self.dxfrx_models.append(item.strip())

        except Exception as error:  # (ConfigParser.Error, IOError):
            # Make a new settings file, because we couldn't read the old one
            print error
            try:
                self.create_config_file()
                self.read_config_file()
            except Exception as error:
                print error
                pass
        return

    def create_config_file(self):
        """Creates a new config file"""
        self.config_fail = True
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        try:
            if os.path.exists(self.path + 'settings.txt'):
                os.remove(self.path + 'settings.txt')
        except OSError:
            pass
        with open((self.path + "settings.txt"), 'w') as config_file:
            config_file.write("")
        config = ConfigParser.RawConfigParser()
        config.add_section('Settings')
        config.set('Settings', 'default master address', '192.168.1.1')
        config.set('Settings', 'default device number', '0')
        config.set('Settings', 'default connection type', 'TCP')
        config.set('Settings', 'default enable dhcp', True)
        config.set('Settings', 'number of threads', 20)
        config.set('Settings', 'telnet client executable', ('putty.exe'))
        config.set('Settings', 'telnet timeout in seconds', '4')
        config.set('Settings',
                   'display notification of successful connections', True)
        config.set('Settings', 'DHCP sniffing enabled', True)
        config.set('Settings', 'filter incoming DHCP for AMX only', False)
        config.set('Settings', 'play sounds', True)
        config.set('Settings', 'check for updates', True)
        config.add_section('Config')
        config.set('Config', 'columns_config', self.columns_default)
        config.set('Config', 'DXLink TX Models', self.dxtx_models_default)
        config.set('Config', 'DXLink RX Models', self.dxrx_models_default)
        config.set(
            'Config', 'DXLink Fibre TX Models', self.dxftx_models_default)
        config.set(
            'Config', 'DXLink Fibre RX Models', self.dxfrx_models_default)
        with open((self.path + "settings.txt"), 'w') as configfile:
            config.write(configfile)

    def write_config_file(self):
        """Update values in config file"""
        config = ConfigParser.RawConfigParser()
        config.read((self.path + "settings.txt"))
        config.set('Settings', 'default master address', self.master_address)
        config.set('Settings', 'default device number', self.device_number)
        config.set('Settings', 'default connection type',
                   self.default_connection_type)
        config.set('Settings', 'default enable dhcp', self.default_dhcp)
        config.set('Settings', 'number of threads', self.thread_number)
        config.set('Settings', 'telnet client executable', self.telnet_client)
        config.set('Settings', 'telnet timeout in seconds',
                   self.telnet_timeout_seconds)
        config.set('Settings', 'DHCP sniffing enabled', self.dhcp_sniffing)
        config.set('Settings', 'filter incoming DHCP for AMX only',
                   self.amx_only_filter)
        config.set('Settings', 'play sounds', self.play_sounds)
        config.set('Settings', 'check for updates', self.check_for_updates)
        columns = ''
        for item in self.columns_config:
            columns = columns + item + ', '
        columns = columns[:-2]
        config.set('Config', 'columns_config', columns)
        with open((self.path + "settings.txt"), 'w') as configfile:
            config.write(configfile)

    def check_for_telnet_client(self):
        """Checks if telnet client in the path"""
        if not os.path.exists(self.path + self.telnet_client):
            self.telnet_missing = True

    def telnet_missing_dia(self):
        """Show dialog for missing putty"""
        dlg = wx.MessageDialog(
            parent=self,
            message='I notice that you don\'t have a copy of putty.exe \n' +
            'available. Click OK to automatically download this \n' +
            'telnet client.',
            caption='Auto download',
            style=wx.OK | wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            # download
            putty_url = ('http://the.earth.li/' +
                         '~sgtatham/putty/latest/x86/putty.exe')
            try:
                # resp = requests.head(putty_url)
                # if resp.status_code != 404:
                Thread(target=urllib.urlretrieve,
                       args=(putty_url, self.path + 'putty.exe')).start()
                dlg.Destroy()
                return
            except:
                dlg.Destroy()
        dlg = wx.MessageDialog(
            parent=self,
            message=('Please manually copy ' +
                     self.path +
                     ' \nThis will allow you to telnet to a device.'),
            caption='No telnet client',
            style=wx.OK)

        dlg.ShowModal()
        dlg.Destroy()

    def set_title_bar(self):
        """Sets title bar text"""
        self.SetTitle(self.name + " " + self.version)

    def configure_device(self, _):
        """Configures a DXLink devices ip master and device number"""
        if self.check_for_none_selected():
            return
        self.configure_list = []
        self.dev_inc_num = int(self.device_number)

        for obj in self.main_list.GetSelectedObjects():
            self.set_status((obj, "Configuring"))
            self.configure_list.append(obj)
            if self.device_number == "0":
                self.dev_inc_num = 0
            dia = config_menus.DeviceConfig(self, obj, str(self.dev_inc_num))
            dia.ShowModal()
            dia.Destroy()
            self.dev_inc_num += 1
            if self.abort is True:
                self.abort = False
                return
        if self.configure_list == []:
            return

    def configure_prefs(self, _):
        """Sets user Preferences"""
        dia = config_menus.PreferencesConfig(self)
        dia.ShowModal()
        dia.Destroy()

    def load_data_pickle(self):
        """Loads main list from data file"""
        if os.path.exists(self.path + 'data_' + self.version + '.pkl'):
            try:
                with open((self.path + 'data_' + self.version + '.pkl'),
                          'rb') as data_file:
                    objects = pickle.load(data_file)
                    self.main_list.SetObjects(objects)
            except (IOError, KeyError):
                self.new_pickle()
        self.main_list.SetSortColumn(0, resortNow=True)

    def new_pickle(self):
        """Creates a new pickle if there is a problem with the old one"""
        try:
            if os.path.exists((self.path + 'data_' + self.version + '.pkl')):
                os.rename(self.path + 'data_' + self.version + '.pkl',
                          self.path + 'data_' + self.version + '.bad')
        except IOError:
            dlg = wx.MessageDialog(parent=self, message='There is a problem ' +
                                   'with the .pkl data file. Please delete ' +
                                   'to continue. ' +
                                   ' The program will now exit',
                                   caption='Problem with .pkl file',
                                   style=wx.OK)
            dlg.ShowModal()
            self.Destroy()

    def resize_frame(self):
        """Resizes the Frame"""
        panel_width = self.panel_width_offset
        columns = ['Time', 'IP', 'Status']
        if self.columns_config != ['']:
            columns += self.columns_config
        for item in columns:
            panel_width += self.col_width[item]
        if panel_width < self.min_panel_width:
            panel_width = self.min_panel_width
        self.SetSize((panel_width, 600))

    def update_status_bar(self):
        """Updates the status bar."""
        self.status_bar.SetFieldsCount(4)

        master_width = wx.ClientDC(self.status_bar).\
            GetTextExtent(self.master_address)[0] + 0
        device_width = wx.ClientDC(self.status_bar).\
            GetTextExtent(self.device_number)[0] + 0
        self.status_bar.SetStatusWidths([-1, master_width,
                                         device_width, 30])
        self.status_bar.SetStatusText(self.master_address, 1)
        self.status_bar.SetStatusText(self.device_number, 2)

    def on_close(self, _):
        """Close program if user closes window"""
        self.dhcp_listener.shutdown = True
        self.ping_active = False
        self.dump_pickle()
        self.Hide()
        if self.ping_window is not None:
            self.ping_window.Hide()

        self.mse_active_list = []
        self.telnet_job_queue.join()
        self.Destroy()

    def on_quit(self, _):
        """Save list and close the program"""
        self.on_close(None)

    def on_about_box(self, _):
        """Show the About information"""

        description = """Magic DXLink Configurator is an tool for configuring
DXLINK Devices. Features include a DHCP monitor,
import and export csv files, batch ip listing,
serial number extraction, reboots and more.
"""

        licence = """The MIT License (MIT)

Copyright (c) 2014 Jim Maciejewski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

        info = wx.AboutDialogInfo()
        info.SetName(self.name)
        info.SetVersion(self.version)
        info.SetDescription(description)
        info.SetLicence(licence)
        info.AddDeveloper('Jim Maciejewski')
        wx.AboutBox(info)

    def on_beer_box(self, _):
        """ Buy me a beer! Yea!"""
        dlg = wx.MessageDialog(parent=self, message='If you enjoy this ' +
                               'program \n Learn how you can help out',
                               caption='Buy me a beer',
                               style=wx.OK)
        if dlg.ShowModal() == wx.ID_OK:
            url = 'http://ornear.com/give_a_beer'
            webbrowser.open_new_tab(url)
        dlg.Destroy()


def show_splash():
    """create, show and return the splash screen"""
    bitmap = wx.Bitmap('media/splash.jpg')
    splash = wx.SplashScreen(
        bitmap, wx.SPLASH_CENTRE_ON_SCREEN, 1700, None, -1)
    splash.Show()
    return splash


def main():
    """run the main program"""
    dxlink_configurator = wx.App()  # redirect=True, filename="log.txt")
    # splash = show_splash()

    # do processing/initialization here and create main window
    dxlink_frame = MainFrame(None)
    dxlink_frame.Show()
    # splash.Destroy()

    if dxlink_frame.config_fail is True:
        dxlink_frame.config_fail_dia()
    if dxlink_frame.telnet_missing is True:
        dxlink_frame.telnet_missing_dia()
    dxlink_configurator.MainLoop()

if __name__ == '__main__':
    main()
