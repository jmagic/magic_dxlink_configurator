"""Configurator is a program that integrates device discovery and telnet
commands to ease configuration and management of AMX DXLink devices.

The MIT License (MIT)

Copyright (c) 2019 Jim Maciejewski

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

import os
import sys
import datetime
import pickle
import wx
import csv
from ObjectListView import FastObjectListView as ObjectListView, ColumnDefn, EVT_CELL_EDIT_FINISHING
import queue
import webbrowser
import requests
import random
from dataclasses import dataclass, field
from pydispatch import dispatcher
from threading import Thread
from shutil import which
from netaddr import IPRange, IPNetwork

from scripts import (auto_update, config_menus, dhcp_sniffer, mdc_gui, send_command,
                     multi_ping, multi_ping_model, mse_baseline, telnet_class, telnetto_class,
                     dipswitch)


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


class DXLink_Configurator_Frame(mdc_gui.DXLink_Configurator_Frame):
    def __init__(self, parent):
        mdc_gui.DXLink_Configurator_Frame.__init__(self, parent)

        icon_bundle = wx.IconBundle()
        icon_bundle.AddIcon(os.path.join("icon", "MDC_icon.ico"), wx.BITMAP_TYPE_ANY)
        self.SetIcons(icon_bundle)
        self.name = "Magic DXLink Configurator"
        self.version = "v4.0.1"
        self.storage_path = os.path.expanduser(os.path.join('~', 'Documents', self.name))
        self.storage_file = "_".join(self.name.split()) + ".pkl"
        self.SetTitle(self.name + " " + self.version)

        pick = self.load_config()
        self.preferences = pick['preferences']
        self.preferences.set_prefs(self.storage_path)
        if self.preferences.telnet_client is None:
            self.telnet_missing_dia()

        self.main_list = ObjectListView(self.olv_panel, wx.ID_ANY,
                                        style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.main_list.cellEditMode = ObjectListView.CELLEDIT_DOUBLECLICK
        self.main_list.Bind(EVT_CELL_EDIT_FINISHING, self.save_main_list)
        self.main_list.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,
                            self.olv_panelOnContextMenu)
        self.main_list.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

        self.columns = [
            ColumnDefn("Time", "right", 110, "arrival_time", stringConverter="%I:%M:%S%p"),
            ColumnDefn("Model", "right", 160, "model"),
            ColumnDefn("MAC", "right", 125, "mac_address"),
            ColumnDefn("IP", "right", 120, "ip_address"),
            ColumnDefn("Hostname", "right", 150, "hostname"),
            ColumnDefn("Serial", "right", 150, "serial"),
            ColumnDefn("Firmware", "right", 100, "firmware"),
            ColumnDefn("Device", "right", 80, "device"),
            ColumnDefn("Static", "center", 30, "ip_type"),
            ColumnDefn("Master", "right", 120, "master"),
            ColumnDefn("System", "center", 80, "system"),
            ColumnDefn("Status", "center", 120, "status")]

        self.set_selected_columns()
        self.main_list.SetEmptyListMsg("Select Tools-->Add Item to add an individual item")
        self.olv_sizer.Add(self.main_list, 1, wx.ALL | wx.EXPAND, 0)
        self.olv_sizer.Layout()

        for item in pick['main_list']:
            item.status = ""
            self.main_list.AddObject(item)

        # Should these be here?
        self.errorlist = []
        self.completionlist = []
        self.configure_list = []
        self.mse_active_list = []
        self.serial_active = []
        self.port_error = False
        self.cancel = False
        self.abort = False

        self.amx_only_filter_chk.Check(self.preferences.amx_only_filter)
        self.dhcp_sniffing_chk.Check(self.preferences.dhcp_listen)
        self.update_status_bar()

        # What is this used for??
        self.cert_path = self.resource_path('cacert.pem')

        # Create DHCP listening thread
        self.dhcp_listener = dhcp_sniffer.DHCPListener()
        self.dhcp_listener.setDaemon(True)
        self.dhcp_listener.start()

        # create a telenetto thread pool and assign them to a queue
        self.telnet_to_queue = queue.Queue()
        for _ in range(10):
            self.telnet_to_thread = telnetto_class.TelnetToThread(
                self, self.telnet_to_queue)
            self.telnet_to_thread.setDaemon(True)
            self.telnet_to_thread.start()

        # create a telnetjob thread pool and assign them to a queue
        self.telnet_job_queue = queue.Queue()
        for _ in range(int(self.preferences.number_of_threads)):
            self.telnet_job_thread = telnet_class.Telnetjobs(
                self, self.telnet_job_queue)
            self.telnet_job_thread.setDaemon(True)
            self.telnet_job_thread.start()

        self.ping_window = multi_ping.MultiPing(self)
        self.ping_window.Hide()
        self.ping_model = multi_ping_model.MultiPing_Model(self.storage_path)

        dispatcher.connect(self.incoming_dhcp,
                           signal="Incoming DHCP",
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
        self.dhcp_listener.dhcp_sniffing_enabled = self.preferences.dhcp_listen

        self.check_for_updates = True
        dispatcher.connect(self.update_required,
                           signal="Software Update",
                           sender=dispatcher.Any)

        if self.check_for_updates:
            update_thread = auto_update.AutoUpdate(server_url="https://magicsoftware.ornear.com", program_name=self.name, program_version=self.version)
            update_thread.setDaemon(True)
            update_thread.start()

    def resource_path(self, relative):
        return os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(".")),
                            relative)

    def update_required(self, sender, message, url):
        """Show the update page"""
        dlg = wx.MessageDialog(parent=self,
                               message='An update is available. \rWould you like to go to the download page?',
                               caption='Update available',
                               style=wx.OK | wx.CANCEL)

        if dlg.ShowModal() == wx.ID_OK:
            webbrowser.open(url)

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
                self.save_main_list()
            else:
                return
        event.Skip()

    def play_sound(self):
        """Plays a barking sound"""
        sounds_list = []
        if self.preferences.play_sounds:
            if self.preferences.randomize_sounds:
                for file in os.listdir('sounds'):
                    if file.endswith('.wav'):
                        sounds_list.append(file)
                filename = random.choice(sounds_list)
            else:
                filename = 'woof.wav'
            sound = wx.adv.Sound(os.path.join('sounds', filename))
            if sound.IsOk():
                sound.Play(wx.adv.SOUND_ASYNC)
            else:
                wx.MessageBox("Invalid sound file", "Error")

    def set_selected_columns(self):
        """Sets the preferred columns"""
        todisplay = []
        for item in self.columns:
            if item.title in self.preferences.cols_selected:
                todisplay.append(item)
        self.main_list.SetColumns(todisplay)
        self.SetSize((self.main_list.GetBestSize()[0] + 40, 600))

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
        self.preferences.dhcp_listen = not self.preferences.dhcp_listen
        self.dhcp_sniffing_chk.Check(self.preferences.dhcp_listen)
        # self.dhcp_listener.dhcp_sniffing_enabled = self.preferences.dhcp_listen
        self.save_main_list()

    def on_amx_only_filter(self, _):
        """Turns amx filtering on and off"""
        self.preferences.amx_only_filter = not self.preferences.amx_only_filter
        self.amx_only_filter_chk.Check(self.preferences.amx_only_filter)
        self.save_main_list()

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

        if self.preferences.telnet_client is not None:

            for obj in self.main_list.GetSelectedObjects():
                self.telnet_to_queue.put([obj, 'telnet'])
                self.set_status((obj, "Queued"))
        else:
            message = f"Putty.exe was not found during startup.\r\rIf you want to telnet to a device you will\r need to download putty.exe to\r {self.storage_path}\r and restart {self.name}"
            dlg = wx.MessageDialog(parent=self,
                                   message=message,
                                   caption='Unable to find putty.exe',
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
        if os.path.exists(os.path.join(self.storage_path, self.telnet_client)):

            for obj in self.main_list.GetSelectedObjects():
                self.telnet_to_queue.put([obj, 'ssh'])
                self.set_status((obj, "Queued"))
        else:
            dlg = wx.MessageDialog(
                parent=self,
                message='Could not find telnet client \nPlease put ' +
                '%s in \n%s' % (self.telnet_client, self.storage_path),
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
                dia = mse_baseline.MSEBaseline(self, obj)
                dia.Show()

    def mse_enable_thread(self, obj):
        """Adds mse thread for plotting / baseline"""
        self.telnet_job_queue.put(['get_dxlink_mse', obj, self.preferences.telnet_timeout])
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
        if obj.model not in self.preferences.dxrx_models:
            dlg = wx.MessageDialog(parent=self, message='This does not ' +
                                   'appear to be a RX device. You can only' +
                                   ' get MSE values from RX devices. Click ' +
                                   'OK to continue anyway.',
                                   caption='MSE only works on RX devices',
                                   style=wx.OK | wx.CANCEL)
            if dlg.ShowModal() != wx.ID_OK:
                dlg.Destroy()
                return False
            dlg.Destroy()
        return True

    def on_dipswitch(self, _):
        """View what the dipswitches do"""
        dia = dipswitch.ShowDipSwitch(self)
        dia.Show()

    def multi_ping(self, event):
        """Ping and track results of many devices --
        Hide and show window if neccesarry"""
        if self.check_for_none_selected():
            return
        self.ping_window.Show()
        self.ping_model.add(self.main_list.GetSelectedObjects())

    def multi_ping_remove(self, obj):
        """Removes an item from multiping"""
        self.ping_model.delete(obj)

    def multi_ping_logging(self):
        self.ping_model.toggle_logging()

    def multi_ping_shutdown(self):
        """Shuts down multi-ping"""
        # pass
        Thread(target=self.ping_model.shutdown).start()
        # self.ping_model.shutdown()
        # pass

    def factory_av(self, _):
        """Reset device AV settings to factory defaults"""
        if self.check_for_none_selected():
            return

        for obj in self.main_list.GetSelectedObjects():
            self.telnet_job_queue.put(['factory_av', obj,
                                       self.preferences.telnet_timeout])
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
                                           self.preferences.telnet_timeout])
                self.set_status((obj, "Queued"))

            else:
                return

    def reboot(self, _):
        """Reboots device"""
        if self.check_for_none_selected():
            return
        for obj in self.main_list.GetSelectedObjects():
            self.telnet_job_queue.put(['reboot', obj,
                                       self.preferences.telnet_timeout])
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
                                       self.preferences.telnet_timeout])
            self.set_status((obj, "Queued"))

    def turn_on_leds(self, _):
        """Turns on front panel LEDs"""
        if self.check_for_none_selected():
            return
        for obj in self.main_list.GetSelectedObjects():
            self.telnet_job_queue.put(['turn_on_leds', obj,
                                       self.preferences.telnet_timeout])
            self.set_status((obj, "Queued"))

    def turn_off_leds(self, _):
        """Turns off front panel LEDs"""
        if self.check_for_none_selected():
            return
        for obj in self.main_list.GetSelectedObjects():
            self.telnet_job_queue.put(['turn_off_leds', obj,
                                       self.preferences.telnet_timeout])
            self.set_status((obj, "Queued"))

    def on_gen_dgx_100(self, event):
        """Generates a list of IP's for the 100 series"""
        item_id = event.GetId()
        menu = event.GetEventObject()
        menuItem = menu.FindItemById(item_id)
        num_of_devices = str((int(menuItem.GetItemLabelText().split()[1]) // 100))
        # print('num of ', num_of_devices)

        ip_range = IPRange('198.18.130.1', '198.18.130.' + num_of_devices)
        # print 'ip_range: ', ip_range
        for address in list(ip_range):
            self.main_list.AddObject(DXLinkUnit(ip_address=str(address)))
        ip_range = IPRange('198.18.134.1', '198.18.134.' + num_of_devices)
        for address in list(ip_range):
            self.main_list.AddObject(DXLinkUnit(ip_address=str(address)))
        self.save_main_list()

    def enable_wd(self, _):
        """Enables the Watchdog"""
        if self.check_for_none_selected():
            return
        for obj in self.main_list.GetSelectedObjects():
            self.telnet_job_queue.put(['set_watchdog', obj,
                                       self.preferences.telnet_timeout, True])
            self.set_status((obj, "Queued"))

    def disable_wd(self, _):
        """disables the Watchdog"""
        if self.check_for_none_selected():
            return
        for obj in self.main_list.GetSelectedObjects():
            self.telnet_job_queue.put(['set_watchdog', obj,
                                       self.preferences.telnet_timeout, False])
            self.set_status((obj, "Queued"))

    def send_commands(self, _):
        """Send commands to selected devices"""
        if self.check_for_none_selected():
            return
        dxtx_devices = []
        dxrx_devices = []
        dxftx_devices = []
        dxfrx_devices = []
        unknown_devices = []
        for obj in self.main_list.GetSelectedObjects():
            if obj.model in self.preferences.dxtx_models:
                dxtx_devices.append(obj)
            elif obj.model in self.preferences.dxrx_models:
                dxrx_devices.append(obj)
            elif obj.model in self.preferences.dxftx_models:
                dxftx_devices.append(obj)
            elif obj.model in self.preferences.dxfrx_models:
                dxfrx_devices.append(obj)
            else:
                unknown_devices.append(obj)

        if len(unknown_devices) > 0:
            dlg = wx.SingleChoiceDialog(parent=self,
                                        message=('Unable to identify what type of dxlink devices have been selected\nIf you are sure these are DXLink devices\n' +
                                                 'please select the apporiate family.\n\nChose carefully, as commands' +
                                                 ' are indetend for specific devices'),
                                        caption='Unable to identify devices',
                                        choices=['DX-TX', 'DX-RX', 'Fiber DX-TX', 'Fiber DX-RX'],
                                        style=wx.OK | wx.CANCEL)
            if dlg.ShowModal() == wx.ID_OK:
                selection = dlg.GetStringSelection()
                if selection == 'DX-TX':
                    dxtx_devices = dxtx_devices + unknown_devices
                elif selection == 'DX-RX':
                    dxrx_devices = dxrx_devices + unknown_devices
                elif selection == 'Fiber DX-TX':
                    dxftx_devices = dxftx_devices + unknown_devices
                elif selection == 'Fiber DX-RX':
                    dxfrx_devices = dxfrx_devices + unknown_devices
            dlg.Destroy()

        if len(dxtx_devices) != 0:
            dia_tx = send_command.SendCommandConfig(self, dxtx_devices, 'dxtx')
            dia_tx.Show()

        if len(dxrx_devices) != 0:
            dia_rx = send_command.SendCommandConfig(self, dxrx_devices, 'dxrx')
            dia_rx.Show()
        if len(dxftx_devices) != 0:
            dia_ftx = send_command.SendCommandConfig(self, dxftx_devices, 'dxftx')
            dia_ftx.Show()

        if len(dxfrx_devices) != 0:
            dia_frx = send_command.SendCommandConfig(self, dxfrx_devices, 'dxfrx')
            dia_frx.Show()

    def export_to_csv(self, _):
        """Store list items in a CSV file"""
        if self.check_for_none_selected():
            return
        save_file_dialog = wx.FileDialog(
            self,
            message='Select file to add devices to or create a new file',
            defaultDir=self.storage_path,
            defaultFile="",
            wildcard="CSV files (*.csv)|*.csv",
            style=wx.FD_SAVE)
        if save_file_dialog.ShowModal() == wx.ID_OK:
            path = save_file_dialog.GetPath()
            with open(path, 'a', newline='') as store_file:
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
            self.save_main_list()

    def import_csv_file(self, _):
        """Imports a list of devices to the main list"""
        open_file_dialog = wx.FileDialog(self, message="Import a CSV file",
                                         defaultDir=self.storage_path,
                                         defaultFile="",
                                         wildcard="CSV files (*.csv)|*.csv",
                                         style=wx.FD_OPEN |
                                         wx.FD_FILE_MUST_EXIST)
        if open_file_dialog.ShowModal() == wx.ID_OK:
            csv_path = open_file_dialog.GetPath()
            open_file_dialog.Destroy()
            dlg = wx.MessageDialog(parent=self, message='To replace ' +
                                   'all items currently in your list,  ' +
                                   'click ok',
                                   caption='Replace items',
                                   style=wx.OK | wx.CANCEL)
            if dlg.ShowModal() == wx.ID_OK:
                self.main_list.DeleteAllItems()

            with open(csv_path, 'r', newline='') as csvfile:
                cvs_data = csv.reader(csvfile)
                for item in cvs_data:
                    data = DXLinkUnit(model=item[0],
                                      hostname=item[1],
                                      serial=item[2],
                                      firmware=item[3],
                                      device=item[4],
                                      mac_address=item[5],
                                      ip_address=item[6],
                                      arrival_time=datetime.datetime.strptime((item[7]), "%Y-%m-%d %H:%M:%S.%f"),
                                      ip_type=item[8],
                                      gateway=item[9],
                                      subnet=item[10],
                                      master=item[11],
                                      system=item[12])

                    self.main_list.AddObject(data)
            self.save_main_list()

        else:
            open_file_dialog.Destroy()

    def import_ip_list(self, _):
        """Imports a list of IP addresses"""
        open_file_dialog = wx.FileDialog(
            self, message="Open IP List",
            defaultDir=self.storage_path,
            defaultFile="",
            wildcard="CSV files (*.csv)|*.csv",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if open_file_dialog.ShowModal() == wx.ID_OK:
            self.main_list.DeleteAllItems()
            with open(open_file_dialog.GetPath(), 'r', newline='') as csvfile:
                cvs_data = csv.reader(csvfile)
                for item in cvs_data:
                    self.main_list.AddObject(DXLinkUnit(ip_address=item[0]))
            self.save_main_list()
            open_file_dialog.Destroy()
        else:
            open_file_dialog.Destroy()

    def import_online_tree_file(self, _):
        """Imports from an online tree report"""
        open_file_dialog = wx.FileDialog(
            self, message="Open Online Tree Report",
            defaultDir=self.storage_path,
            defaultFile="",
            wildcard="TXT files (*.txt)|*.txt",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if open_file_dialog.ShowModal() == wx.ID_OK:
            # self.olv_queue.put(['delete_all_items'])
            with open(open_file_dialog.GetPath(), 'r') as f:
                online_tree = f.read()
            online_tree_list = online_tree.split('+ IPv4 Address.......:')[1:]
            # print online_tree_list[0]
            for item in online_tree_list:
                data = DXLinkUnit(ip_address=item.split()[0], arrival_time=datetime.datetime.now())
                self.main_list.AddObject(data)
            self.save_main_list()
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
        data = DXLinkUnit(arrival_time=datetime.datetime.now())
        self.main_list.AddObject(data)
        self.save_main_list()

    def delete_item(self, _):
        """Deletes the selected item"""
        if len(self.main_list.GetSelectedObjects()) == \
           len(self.main_list.GetObjects()):
            self.main_list.DeleteAllItems()
            self.save_main_list()
            return
        if len(self.main_list.GetSelectedObjects()) == 0:
            return
        self.main_list.RemoveObjects(self.main_list.GetSelectedObjects())
        self.save_main_list()

    def delete_all_items(self, _):
        """Deletes all items,selected or not"""
        dlg = wx.MessageDialog(parent=self, message='Are you sure? \n This ' +
                               'will delete all items in the list',
                               caption='Delete All Items',
                               style=wx.OK | wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            self.main_list.DeleteAllItems()
            self.save_main_list()
        else:
            return

    def new_unit(self):
        return DXLinkUnit()

    def dhcp_on_status_bar(self, obj, incoming_time):
        self.status_bar.SetStatusText(
            incoming_time.strftime('%I:%M:%S%p') +
            ' -- ' + obj.hostname +
            ' ' + obj.ip_address +
            ' ' + obj.mac_address)

    def incoming_dhcp(self, sender):
        """Receives dhcp requests and adds them to objects to display"""
        incoming_time = datetime.datetime.now()
        hostname, mac_address, ip_address = sender
        # print('got dhcp: ', mac_address)

        # Check if it is filtered
        if not self.preferences.dhcp_listen:
            # print('no listen')
            return
        if bool(self.preferences.amx_only_filter):
            if mac_address[0:8] != '00:60:9f':
                # print('not amx mac')
                obj = DXLinkUnit(hostname=hostname, mac_address=mac_address, ip_address=ip_address)
                self.dhcp_on_status_bar(obj, incoming_time)
                return
        if self.preferences.subnet_filter_enable:
            if ip_address not in IPNetwork(self.preferences.subnet_filter):
                # print('no subnet')
                obj = DXLinkUnit(hostname=hostname, mac_address=mac_address, ip_address=ip_address)
                self.dhcp_on_status_bar(obj, incoming_time)
                return

        # Check if duplicate in list
        duplicate_list = []
        for obj in self.main_list.GetObjects():
            if obj.mac_address == mac_address:
                # print('duplicate')
                duplicate_list.append(obj)

        # Add or update list
        if duplicate_list != []:
            # remove duplicates
            if len(duplicate_list) > 1:
                for item in duplicate_list[1:]:
                    self.main_list.RemoveObject(item)
            # update duplicate with new info
            obj = duplicate_list[0]
            obj.ip_address = ip_address
            obj.hostname = hostname
            obj.arrival_time = incoming_time

        else:
            # new item
            obj = DXLinkUnit(hostname=sender[0], mac_address=sender[1], ip_address=sender[2], arrival_time=incoming_time)
            self.main_list.AddObject(obj)
            self.set_status((obj, "DHCP"))

        if obj.hostname[:2] == 'DX':
            # Need to check if we have updated DXLink device recently
            # print(incoming_time - obj.last_status)
            # print(incoming_time - obj.last_status < datetime.timedelta(seconds=2))
            if (incoming_time - obj.last_status) < datetime.timedelta(seconds=2):
                # print('no check')
                pass
            else:
                # print('checking')
                obj.last_status = incoming_time
                self.telnet_job_queue.put(['get_config_info', obj,
                                           self.preferences.telnet_timeout])
        self.dhcp_on_status_bar(obj, incoming_time)
        self.main_list.Refresh()
        self.save_main_list()
        self.play_sound()

    def save_main_list(self, event=None):
        """Saves the preference and main list"""
        self.save_config(preferences=self.preferences)

    def load_config(self):
        """Load Config"""
        try:
            with open(os.path.join(self.storage_path, self.storage_file), 'rb') as f:
                pick = pickle.load(f)
            return pick
        except Exception as error:
            print('unable to load plk ', error)
            # self.save_config()
            pick = {'preferences': Preferences(), 'main_list': []}
            return pick

    def save_config(self, preferences=None, gui_preferences=None):
        """Update values in config file"""
        # print('saving...')
        if preferences is None:
            # Create new config file
            preferences = Preferences()
        if not os.path.exists(self.storage_path):
            os.mkdir(self.storage_path)
        with open(os.path.join(self.storage_path, self.storage_file), "wb") as f:
            pick = {'preferences': preferences, 'main_list': self.main_list.GetObjects()}
            pickle.dump(pick, f)

    def telnet_missing_dia(self):
        """Show dialog for missing putty"""
        putty_path = os.path.join(self.storage_path, 'putty.exe')
        message = f'I\'m unable to find putty.exe in your path.\r\rClick OK to automatically download putty.exe telnet client.\r\rSaving here: {putty_path}'
        dlg = wx.MessageDialog(
            parent=self,
            message=message,
            caption='Auto download',
            style=wx.OK | wx.CANCEL)
        if dlg.ShowModal() != wx.ID_OK:
            return
        dlg.Destroy()

        # download
        putty_url = ('http://the.earth.li/' +
                     '~sgtatham/putty/latest/x86/putty.exe')
        try:
            with open(os.path.join(self.storage_path, 'putty.exe'), "wb") as f:

                response = requests.get(putty_url, stream=True)
                total_length = response.headers.get('content-length')

                if total_length is None:  # no content length header
                    f.write(response.content)
                else:
                    dlg = wx.ProgressDialog("Downloading Putty.exe",
                                            "Progress",
                                            maximum=int(total_length),
                                            parent=self,
                                            style=wx.PD_CAN_ABORT | wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME | wx.PD_ESTIMATED_TIME | wx.PD_REMAINING_TIME)
                    dl = 0
                    total_length = int(total_length)
                    for data in response.iter_content(chunk_size=1024):
                        dl += len(data)
                        f.write(data)
                        dlg.Update(dl)

                dlg.Destroy()
                self.preferences.set_prefs(self.storage_path)
                return
        except Exception as error:
            print('Error downloading: ', error)
            if os.path.exists(os.path.join(self.storage_path, 'putty.exe')):
                os.remove(os.path.join(self.storage_path, 'putty.exe'))
            try:
                dlg.Destroy()
            except Exception as error:
                print('Error: ', error)
        dlg = wx.MessageDialog(
            parent=self,
            message=('Unable to download putty.exe\r\rPlease manually copy putty.exe to ' +
                     self.storage_path +
                     '\r\rThis will allow you to telnet to a device.'),
            caption='No telnet client',
            style=wx.OK)

        dlg.ShowModal()
        dlg.Destroy()

    def configure_device(self, _):
        """Configures a DXLink devices ip master and device number"""
        if self.check_for_none_selected():
            return
        self.configure_list = []
        self.dev_inc_num = int(self.preferences.device_number)

        for obj in self.main_list.GetSelectedObjects():
            self.set_status((obj, "Configuring"))
            self.configure_list.append(obj)
            if self.preferences.device_number == 0:
                self.dev_inc_num = 0
            dia = config_menus.DeviceConfig(self, obj, str(self.dev_inc_num))
            dia.ShowModal()
            dia.Destroy()
            self.dev_inc_num += 1
            if self.cancel is True:
                self.cancel = False
                self.set_status((obj, ""))
            if self.abort is True:
                self.abort = False
                self.set_status((obj, ""))
                return
        if self.configure_list == []:
            return

    def configure_prefs(self, _):
        """Sets user Preferences"""
        dia = config_menus.PreferencesConfig(self)
        dia.ShowModal()
        dia.Destroy()
        self.update_status_bar()
        self.set_selected_columns()

    def update_status_bar(self):
        """Updates the status bar."""
        self.status_bar.SetFieldsCount(4)

        master_width = wx.ClientDC(self.status_bar).\
            GetTextExtent(self.preferences.master_address)[0] + 0
        device_width = wx.ClientDC(self.status_bar).\
            GetTextExtent(str(self.preferences.device_number))[0] + 0
        self.status_bar.SetStatusWidths([-1, master_width,
                                         device_width, 30])
        self.status_bar.SetStatusText(self.preferences.master_address, 1)
        self.status_bar.SetStatusText(str(self.preferences.device_number), 2)

    def on_close(self, event):
        self.save_main_list()
        dispatcher.send(signal="Shutdown")
        event.Skip()

    def on_exit(self, event):
        self.save_main_list()
        dispatcher.send(signal="Shutdown")
        self.Close()

    def on_about_box(self, _):
        """Show the About information"""

        description = """Magic DXLink Configurator is an tool for configuring
DXLINK Devices. Features include a DHCP monitor,
import and export csv files, batch ip listing,
serial number extraction, reboots and more.
"""

        licence = """The MIT License (MIT)

Copyright (c) 2019 Jim Maciejewski

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

        info = wx.adv.AboutDialogInfo()
        info.SetName(self.name)
        info.SetVersion(self.version)
        info.SetDescription(description)
        info.SetLicence(licence)
        info.AddDeveloper('Jim Maciejewski')
        wx.adv.AboutBox(info)

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


# def show_splash():
#     """create, show and return the splash screen"""
#     bitmap = wx.Bitmap('media/splash.jpg')
#     splash = wx.SplashScreen(
#         bitmap, wx.SPLASH_CENTRE_ON_SCREEN, 1700, None, -1)
#     splash.Show()
#     return splash


def main():
    """run the main program"""
    dxlink_configurator = wx.App()  # redirect=True, filename="log.txt")
    # splash = show_splash()
    # do processing/initialization here and create main window
    dxlink_frame = DXLink_Configurator_Frame(None)
    dxlink_frame.Show()
    dxlink_configurator.MainLoop()


if __name__ == '__main__':
    main()
