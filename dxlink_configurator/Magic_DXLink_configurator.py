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
import time
import os
import csv
from ObjectListView import ObjectListView, ColumnDefn
import Queue
import webbrowser


from pydispatch import dispatcher

from scripts import (config_menus, dhcp_sniffer, mdc_gui, multi_send, 
                     multi_ping, mse_baseline, plot_class, telnet_class,
                     telnetto_class)

try:
    import winsound
except ImportError:
    pass



########################################################################
class Unit(object):
    """
    Model of the Unit

    Contains the following attributes:
    model, hostname, serial ,firmware, device, mac, ip, time, ip_type, gateway,
    subnet, master, system
    """
    #----------------------------------------------------------------------
    def __init__(self,  model, hostname, serial ,firmware, device, mac, ip_ad, \
                 arrival_time, ip_type, gateway, subnet, master, system):

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


#class MainPanel(wx.Panel):

class MainFrame(mdc_gui.MainFrame):
    def __init__(self, parent):
        mdc_gui.MainFrame.__init__(self, parent)

        self.parent = parent

        icon_bundle = wx.IconBundle()
        icon_bundle.AddIconFromFile(r"icon\MDC_icon.ico", wx.BITMAP_TYPE_ANY)
        self.SetIcons(icon_bundle)

        self.master_address = None
        self.device_number = None
        self.default_dhcp = None
        self.thread_number = None
        self.telnet_client = None
        self.telnet_timeout_seconds = None
        self.displaysuccess = None
        self.dhcp_sniffing = None
        self.amx_only_filter = None
        self.play_sounds = None
        self.columns_config = None
        if os.name == 'nt':
            self.path = os.path.expanduser(
                '~\\Documents\\Magic_DXLink_Configurator\\')
        else:
            self.path = os.path.expanduser(
                '~/Documents/Magic_DXLink_Configurator/')
        self.read_config_file()
        self.resize_frame()
        self.name = "Magic DXLink Configurator"
        self.version = "v3.x.x"

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

        self.main_list = ObjectListView(self.olv_panel, wx.ID_ANY, 
                                        style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.main_list.cellEditMode = ObjectListView.CELLEDIT_DOUBLECLICK
        self.main_list.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, 
                            self.MainFrameOnContextMenu)
        self.main_list.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

        self.columns = []
        self.columns_setup = [ColumnDefn("Time", "center", 90, "arrival_time", 
                                         stringConverter="%I:%M:%S%p"),
                              ColumnDefn("Model", "center", 130, "model"),
                              ColumnDefn("MAC", "center", 130, "mac_address"),
                              ColumnDefn("IP", "center", 100, "ip_address"),
                              ColumnDefn("Hostname", "left", 130, "hostname"),
                              ColumnDefn("Serial", "center", 130, "serial"),
                              ColumnDefn("Firmware", "center", 80, "firmware"),
                              ColumnDefn("Device", "center", 80, "device"),
                              ColumnDefn("Static", "center", 60, "ip_type"),
                              ColumnDefn("Master", "center", 100, "master"),
                              ColumnDefn("System", "center", 80, "system")
                             ]

        self.select_columns()
        self.load_data_pickle()
        self.update_status_bar()

        self.olv_sizer.Add(self.main_list, 1, wx.ALL|wx.EXPAND, 5)

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
        dispatcher.connect(self.collect_completions,
                           signal="Collect Completions", 
                           sender=dispatcher.Any)
        dispatcher.connect(self.collect_errors, 
                           signal="Collect Errors", 
                           sender=dispatcher.Any)
    #----------------------------------------------------------------------

    def on_key_down(self, event):
        """Grab Delete key presses"""
        key = event.GetKeyCode()
        if key == wx.WXK_DELETE:
            dlg = wx.MessageDialog(
                parent=self,
                message=
                'Are you sure? \n\nThis will delete all selected items in ' +
                'the list',
                caption='Delete All Selected Items',
                style=wx.OK|wx.CANCEL)

            if dlg.ShowModal() == wx.ID_OK:
                self.delete_item(None)
                self.dump_pickle()
            else:
                return
        event.Skip()

    def play_sound(self):
        """Plays a barking sound"""
        if self.play_sounds:
            try:
                winsound.PlaySound("sounds\\woof.wav", winsound.SND_FILENAME)
            except IOError:
                pass

    def collect_completions(self, sender):
        """Creates a list of completed connections"""
        self.completionlist.append(sender)

    def collect_errors(self, sender):
        """Creates a list of incomplete connections"""
        self.errorlist.append(sender)

    def port_errors(self):
        """Shows when the listening port is in use"""
        dlg = wx.MessageDialog(
            self,
            message='Unable to use port 67\n No DHCP requests will be added.',
            caption='Port in use',
            style=wx.ICON_INFORMATION)
        dlg.ShowModal()
        self.listenfilter.Enable(False)
        self.listenDHCP.Enable(False)


    def display_progress(self):
        """Shows progress of connections"""
        if len(self.main_list.GetSelectedObjects()) == 1:

            dlg = wx.ProgressDialog(
                'Attempting connect to selected device',
                'Attempting connection to selected device',
                maximum=len(self.main_list.GetSelectedObjects()),
                parent=self,
                style=wx.PD_APP_MODAL
                | wx.PD_AUTO_HIDE
                | wx.PD_SMOOTH)

            while ((len(self.completionlist) + len(self.errorlist)) <
                   len(self.main_list.GetSelectedObjects())):
                count = (len(self.completionlist) + len(self.errorlist))
                #time.sleep(.01)
                dlg.Pulse()
        else:
            dlg = wx.ProgressDialog(
                'Attempting connect to selected devices',
                'Attempting connection to all selected devices',
                maximum=len(self.main_list.GetSelectedObjects()),
                parent=self,
                style=wx.PD_APP_MODAL
                | wx.PD_AUTO_HIDE
                | wx.PD_SMOOTH
                | wx.PD_ELAPSED_TIME)

            while ((len(self.completionlist) + len(self.errorlist)) <
                   len(self.main_list.GetSelectedObjects())):
                count = (len(self.completionlist) + len(self.errorlist))
                dlg.Update(count, "Attempting connection to %s of %s devices" %
                           ((count + 1), 
                            len(self.main_list.GetSelectedObjects())))

        dlg.Destroy()
        errortext = ""
        phil = " "
        
        for i in xrange(len(self.errorlist)):
            while (len(self.errorlist[i][0]) + (len(phil) - 1)) < 15:
                phil = phil + " "
            errortext = errortext + self.errorlist[i][0] + " " + phil + " " +  \
                        self.errorlist[i][1] + "\n"
            phil = " "

        completiontext = ""
        for i in range(len(self.completionlist)):
            completiontext = completiontext + self.completionlist[i][0] + "\n"
        
        if len(self.errorlist) == len(self.main_list.GetSelectedObjects()):
            dlg = wx.MessageDialog(
                parent=self,
                message='Failed to connect to \n=======================' + 
                ' \n%s ' % errortext,
                caption='Failed connection list',
                style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        elif len(self.completionlist) == \
             len(self.main_list.GetSelectedObjects()):
            if self.displaysuccess:
                dlg = wx.MessageDialog(
                    parent=self,
                    message='Successfully connected to: \n' +
                    '=======================\n%s' % completiontext,
                    caption='Connection list',
                    style=wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
        else:
            dlg = wx.MessageDialog(
                parent=self, 
                message='Failed to connect to: \n======================= ' +
                '\n%s \n \n' % (errortext) +
                'Successfully connected to: \n=======================' +
                ' \n%s' % (completiontext),
                caption='Connection list',
                style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        self.main_list.RefreshObjects(self.main_list.GetObjects())
        self.dump_pickle()
        self.errorlist = []
        self.completionlist = []

    def toggle_dhcp_sniffing(self, _):
        """Turns sniffing on and off"""

        self.dhcp_sniffing = not self.dhcp_sniffing
        self.write_config_file()


    def toggle_filter_amx(self, _):
        """Turns amx filtering on and off"""

        self.amx_only_filter = not self.amx_only_filter
        self.write_config_file()

    def select_columns(self):
        """Sets the columns to be displayed"""

        self.columns = []
        for i in range(len(self.columns_setup)):
            self.columns.append((int(self.columns_config[i]),
                                 self.columns_setup[i]))
        todisplay = []
        for item in self.columns:
            if item[0] == 1:
                todisplay.append(item[1])
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

    def on_select_all(self, _):
        """Select all items in the list"""
        self.main_list.SelectAll()

    def on_select_none(self, _):
        """Select none of the items in the list"""
        self.main_list.DeselectAll()


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
        if os.name == 'nt':
            if os.path.exists((self.path + self.telnet_client)):

                for obj in self.main_list.GetSelectedObjects():
                    self.telnet_to_queue.put(obj)
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

        if os.name == 'posix':
            for obj in self.main_list.GetSelectedObjects():
                self.telnet_to_queue.put(obj)

    def plot_mse(self, _):
        """Plots mse over time"""
        if self.check_for_none_selected(): 
            return
        if len(self.main_list.GetSelectedObjects()) > 16:
            dlg = wx.MessageDialog(
                parent=self, message='I can only graph 16 devices at a time ' +
                '\nPlease select less than sixteen devices at once',
                caption='How many graphs?',
                style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return

        dlg = wx.MessageDialog(
            parent=self, message='Warning: MSE values may intermittently ' +
            'show values at -5 or -6.\n\nYou can safely ignore these values.' +
            '\n\nIf you want to verify your MSE baseline please use the \"MSE' +
            ' baseline\" under the tools menu.',
            caption=('Warning MSE values may intermittently show low values '),
            style=wx.OK|wx.ICON_EXCLAMATION)

        dlg.ShowModal()
        dlg.Destroy()
        for obj in self.main_list.GetSelectedObjects():
            if self.mse_rx_check(obj):
                if not self.mse_in_active(obj):
                    self.mse_enable_thread(obj)
                else:
                    if obj.ip_address[:3] == "COM":
                        self.serial_active.append(obj.mac_address)
                self.mse_active_list.append(obj.mac_address)
                dia = plot_class.Multi_Plot(self, obj, '-1500')
                dia.Show()

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
                else:
                    if obj.ip_address[:3] == "COM":
                        self.serial_active.append(obj.mac_address)
                self.mse_active_list.append(obj.mac_address)
                dia = mse_baseline.MSE_Baseline(self, obj)
                dia.Show()

    def mse_enable_thread(self, obj):
        """Adds mse thread for plotting / baseline"""
        if obj.ip_address[:3] == "COM":
            self.serial_active.append(obj.mac_address)
            self.telnet_job_queue.put(['get_dgx_mse', obj, 
                                       self.telnet_timeout_seconds])
        else:
            self.telnet_job_queue.put(['get_dxlink_mse', obj,
                                       self.telnet_timeout_seconds])

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
        if obj.model[12:14] != 'RX' and obj.ip_address[:3] != "COM":
            dlg = wx.MessageDialog(parent=self, message='This does not ' +
                                   'appear to be a RX device. You can only' +
                                   ' get MSE values from RX devices. Click ' +
                                   'OK to continue anyway.',
                                   caption='MSE only works on RX devices',
                                   style=wx.OK|wx.CANCEL)
            if dlg.ShowModal() != wx.ID_OK:
                dlg.Destroy()
                return False
            dlg.Destroy()
        return True

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
        self.display_progress()


    def reset_factory(self, _):
        """Reset device to factory defaults"""
        if self.check_for_none_selected():
            return
        for obj in self.main_list.GetSelectedObjects():
            dlg = wx.MessageDialog(parent=self, message='Are you sure? \n ' +
                                   'This will reset %s' % obj.ip_address,
                                   caption='Factory Reset',
                                   style=wx.OK|wx.CANCEL)
            if dlg.ShowModal() == wx.ID_OK:
                dlg.Destroy()
                self.telnet_job_queue.put(['reset_factory', obj, 
                                           self.telnet_timeout_seconds])
            else:
                return
        self.display_progress()


    def reboot(self, _):
        """Reboots device"""
        if self.check_for_none_selected():
            return
        for obj in self.main_list.GetSelectedObjects():
            self.telnet_job_queue.put(['reboot', obj,
                                       self.telnet_timeout_seconds])
        self.display_progress()


    def open_url(self, _):
        """Opens ip address in a browser""" 
        if self.check_for_none_selected():
            return
        for obj in self.main_list.GetSelectedObjects():
            url = 'http://' + obj.ip_address
            webbrowser.open_new_tab(url)


    def get_config_info(self, _):
        """Connects to device via telnet and gets serial model and firmware """
        if self.check_for_none_selected():
            return
        for obj in self.main_list.GetSelectedObjects():
            self.telnet_job_queue.put(['get_config_info', obj,
                                       self.telnet_timeout_seconds])
        self.display_progress()

    def turn_on_leds(self, _):
        """Turns on front panel LEDs"""
        if self.check_for_none_selected():
            return
        for obj in self.main_list.GetSelectedObjects():
            self.telnet_job_queue.put(['turn_on_leds', obj,
                                       self.telnet_timeout_seconds])
        self.display_progress()

    def turn_off_leds(self, _):
        """Turns off front panel LEDs"""
        if self.check_for_none_selected():
            return
        for obj in self.main_list.GetSelectedObjects():
            self.telnet_job_queue.put(['turn_off_leds', obj,
                                       self.telnet_timeout_seconds])
        self.display_progress()

    def send_commands(self, _):
        """Send commands to selected devices"""
        if self.check_for_none_selected():
            return
        tx_devices = []
        rx_devices = []
        for obj in self.main_list.GetSelectedObjects():
            if obj.model[12:14] == 'TX' or \
               obj.model[12:14] == 'WP' or \
               obj.model[12:15] == 'DWP'or \
               obj.model[12:16] == 'MFTX':
                tx_devices.append(obj)
            elif obj.model[12:14] == 'RX':
                rx_devices.append(obj)
            else:
                pass
        if len(tx_devices) != 0:
            dia = multi_send.MultiSendCommandConfig(self, tx_devices, 'tx')
            dia.ShowModal()
            dia.Destroy()
        if len(rx_devices) != 0:
            dia = multi_send.MultiSendCommandConfig(self, rx_devices, 'rx')
            dia.ShowModal()
            dia.Destroy()
        if (len(tx_devices)+len(rx_devices)) == 0:
            dlg = wx.MessageDialog(parent=self, message='No DXLink Devices' +
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
            dlg = wx.ProgressDialog(
                "Storing Device Information",
                "Storing Device Information",
                maximum=len(self.main_list.GetSelectedObjects()),
                parent=self,
                style=wx.PD_APP_MODAL
                | wx.PD_AUTO_HIDE
                | wx.PD_ELAPSED_TIME)
            count = 0
            with open(path, 'ab') as store_file:
                write_csv = csv.writer(store_file, quoting=csv.QUOTE_ALL)
                for obj in self.main_list.GetSelectedObjects():
                    count += 1
                    dlg.Update(count)
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
                                   style=wx.OK|wx.CANCEL)
            if dlg.ShowModal() == wx.ID_OK:            
                self.main_list.DeleteAllItems()

            with open(open_file_dialog.GetPath(), 'rb') as csvfile:
                cvs_data = csv.reader(csvfile)
                for item in cvs_data:
                    data = Unit(
                        item[0],
                        item[1],
                        item[2],
                        item[3],
                        item[4],
                        item[5],
                        item[6],
                        datetime.datetime.strptime(
                            (item[7]), "%Y-%m-%d %H:%M:%S.%f"), 
                        item[8],
                        item[9],
                        item[10],
                        item[11],
                        item[12])

                    self.main_list.AddObject(data)
            self.dump_pickle()

        else:
            open_file_dialog.Destroy()

    def import_plot(self, _):
        """Imports plot data for display"""
        open_file_dialog = wx.FileDialog(self, message="Import a plot CSV file",
                                         defaultDir=self.path,
                                         defaultFile="",
                                         wildcard="CSV files (*.csv)|*.csv",
                                         style=wx.FD_OPEN 
                                         | wx.FD_FILE_MUST_EXIST)

        if open_file_dialog.ShowModal() == wx.ID_OK:
            open_file_dialog.Destroy()
            with open(open_file_dialog.GetPath(), 'rb') as csvfile:
                csv_data = csv.reader(csvfile)
                header = csv_data.next()
                plot_object = []
                data = Unit(
                    '',
                    '',
                    '',
                    '',
                    header[7],
                    header[6],
                    header[5],
                    '',
                    '',
                    '',
                    '',
                    '',
                    '')
                plot_object.append(data)
                obj = plot_object[0]
                row_count = (sum(1 for row in csv_data)-1)*-1
                dia = plot_class.Multi_Plot(self, obj, row_count)
                dia.Show()
            # opening it again to start at top
            with open(open_file_dialog.GetPath(), 'rb') as csvfile:  
                csv_data = csv.reader(csvfile)
                header = csv_data.next()
                plot_object = []
                data = Unit(
                    '',
                    '',
                    '',
                    '',
                    header[7],
                    header[6],
                    header[5],
                    '',
                    '',
                    '',
                    '',
                    '',
                    '')

                plot_object.append(data)
                obj = plot_object[0]
                self.mse_active_list.append(obj.mac_address)
                for item in csv_data:
                    mse = []
                    data = []
                    for i in range(4):
                        data.append(item[i+1])
                        #print data
                    mse_time = [datetime.datetime.strptime(
                        (item[0]), '%H:%M:%S.%f'), data]
                    mse.append(mse_time)
                    mse.append(header[5])
                    mse.append(header[6])
                    #print mse
                    #time.sleep(.1)
                    dispatcher.send(signal="Incoming MSE", sender=mse)
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
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        item[0],
                        datetime.datetime.now(),
                        '',
                        '',
                        '',
                        '',
                        '')

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

    def generate_dgx_list(self, _):
        """Generates a list of ip addresses"""
        dia = config_menus.DGXListGen(self)
        dia.ShowModal()
        dia.Destroy()

    def add_line(self, _):
        """Adds a line to the main list"""
        data = Unit(' ',
                    ' ',
                    ' ',
                    ' ',
                    ' ',
                    ' ',
                    ' ',
                    datetime.datetime.now(),
                    ' ',
                    ' ',
                    ' ',
                    ' ',
                    ' '
                   )
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
                               style=wx.OK|wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            self.main_list.DeleteAllItems()
            self.dump_pickle()
        else:
            return

    def incoming_packet(self, sender):
        """Receives dhcp requests with and adds them to objects to display"""
        data = Unit('',
                    sender[0],
                    '',
                    '',
                    '',
                    sender[1],
                    sender[2],
                    datetime.datetime.now(),
                    '',
                    '',
                    '',
                    '',
                    '')

        self.status_bar.SetStatusText(
            data.arrival_time.strftime('%I:%M:%S%p') +
            ' -- ' + data.hostname +
            ' ' + data.ip_address +
            ' ' + data.mac_address)
        if self.amx_only_filter:
            if data.mac_address[0:8] != '00:60:9f':
                return
        selected_items = self.main_list.GetSelectedObjects()
        if self.main_list.GetObjects() == []:
            self.main_list.SetObjects([data])
        else:
            for obj in self.main_list.GetObjects():
                if obj.mac_address == data.mac_address:
                    data.model = obj.model
                    data.serial = obj.serial
                    data.firmware = obj.firmware
                    data.device = obj.device
                    data.ip_type = obj.ip_type
                    data.gateway = obj.gateway
                    data.subnet = obj.subnet
                    data.master = obj.master
                    data.system = obj.system
                    self.main_list.RemoveObject(obj)
            self.main_list.AddObject(data)
        #self.main_list.RepopulateList()
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
            self.default_dhcp = (config.getboolean(
                'Settings', 'default enable DHCP'))
            self.thread_number = (config.get(
                'Settings', 'number of threads'))
            self.telnet_client = (config.get(
                'Settings', 'telnet client executable'))
            self.telnet_timeout_seconds = (config.get(
                'Settings', 'telnet timeout in seconds'))
            self.displaysuccess = (config.getboolean(
                'Settings', 'display notification of successful connections'))
            self.dhcp_sniffing = (config.getboolean(
                'Settings', 'DHCP sniffing enabled'))
            self.amx_only_filter = (config.getboolean(
                'Settings', 'filter incoming DHCP for AMX only'))
            self.play_sounds = (config.getboolean(
                'Settings', 'play sounds'))
            self.columns_config = (config.get('Config', 'columns_config'))
        except (ConfigParser.Error, IOError):   
            # Make a new settings file, because we couldn't read the old one
            self.create_config_file()
            self.read_config_file()
        return

    def create_config_file(self):
        """Creates a new config file"""
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        try:
            #os.path.exists(self.path + 'settings.txt'):
            os.remove(self.path + 'settings.txt')
        except OSError:
            pass
        with open((self.path + "settings.txt"), 'w') as config_file:
            config_file.write("")
        config = ConfigParser.RawConfigParser()
        config.add_section('Settings')
        config.set('Settings', 'default master address', '192.168.1.1')
        config.set('Settings', 'default device number', '10001')
        config.set('Settings', 'default enable dhcp', True)
        config.set('Settings', 'number of threads', 20)
        config.set('Settings', 'telnet client executable', ('puttytel.exe'))
        config.set('Settings', 'telnet timeout in seconds', '4')
        config.set('Settings', 
                   'display notification of successful connections', True)
        config.set('Settings', 'DHCP sniffing enabled', True)
        config.set('Settings', 'filter incoming DHCP for AMX only', False)
        config.set('Settings', 'play sounds', True)
        config.add_section('Config')
        config.set('Config', 
                   'Columns are with a 1 are displayed. ', 
                   'Unless you know what your doing, ' + 
                   'please change these in the application')
        config.set('Config', 'columns_config', '11111111110')
        with open((self.path + "settings.txt"), 'w') as configfile:
            config.write(configfile)

    def write_config_file(self):
        """Update values in config file"""
        config = ConfigParser.RawConfigParser()
        config.read((self.path + "settings.txt"))
        config.set('Settings', 'default master address', self.master_address)
        config.set('Settings', 'default device number', self.device_number)
        config.set('Settings', 'default enable dhcp', self.default_dhcp)
        config.set('Settings', 'number of threads', self.thread_number)
        config.set('Settings', 'telnet client executable', self.telnet_client)
        config.set('Settings', 'telnet timeout in seconds', 
                   self.telnet_timeout_seconds)
        config.set('Settings', 'display notification of successful connections',
                   self.displaysuccess)
        config.set('Settings', 'DHCP sniffing enabled', self.dhcp_sniffing)
        config.set('Settings', 'filter incoming DHCP for AMX only', 
                   self.amx_only_filter)
        config.set('Settings', 'play sounds', self.play_sounds)
        config.set('Config', 'columns_config', self.columns_config)
        with open((self.path + "settings.txt"), 'w') as configfile:
            config.write(configfile)

    def set_title_bar(self):
        """Sets title bar text"""
        self.SetTitle(self.name + " " + self.version)

    def configure_device(self, _):
        """Configures a DXLink devices ip master and device number"""
        if self.check_for_none_selected():
            return

        for obj in self.main_list.GetSelectedObjects():
            self.configure_list.append(obj)
            dia = config_menus.DeviceConfig(self, obj)
            dia.ShowModal()
            dia.Destroy()
            if self.abort == True:
                self.abort = False
                return
        if self.configure_list == []:
            return
        else:
            self.display_progress()


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
                          'rb')  as data_file:
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
        panel_width = 30
        for i in range(len(self.columns_config)):
            columns_width = [90, 130, 130, 100, 130, 150, 80, 80, 60, 100, 80]
            if self.columns_config[i] == '1':
                panel_width = panel_width + columns_width[i]
        if panel_width < 400:
            panel_width = 400
        self.SetSize((panel_width, 600))

    def update_status_bar(self):
        """Updates the status bar."""
        self.status_bar.SetFieldsCount(4)
        master_width = wx.ClientDC(self.status_bar).\
                       GetTextExtent(self.master_address)[0] + 0
        device_width = wx.ClientDC(self.status_bar).\
                       GetTextExtent(self.device_number)[0] + 0
        self.status_bar.SetStatusWidths([-1, master_width, \
                                                device_width, 30])
        self.status_bar.SetStatusText(self.master_address, 1)
        self.status_bar.SetStatusText(self.device_number, 2)

    def on_close(self, _):
        """Close program if user closes window"""
        self.Hide()
        if self.ping_window != None:
            self.ping_window.Hide()
        self.ping_active = False
        self.mse_active_list = []
        self.telnet_job_queue.join()
        self.Destroy()

    def on_quit(self, _):
        """Save list and close the program"""
        self.dump_pickle()
        self.Close()

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
        dlg = wx.MessageDialog(parent=self, message='If you enjoy this ' + \
                               'program \n Learn how you can help out', \
                               caption='Buy me a beer', \
                               style=wx.OK)
        if dlg.ShowModal() == wx.ID_OK:
            url = 'http://ornear.com/give_a_beer'
            webbrowser.open_new_tab(url)
        dlg.Destroy()





########################################################################
'''class MainFrame(wx.Frame):
    #----------------------------------------------------------------------
    def __init__(self):

        self.title_text = "Starting up"
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, 
                          title=self.title_text, size=(1100, 600))

        icon_bundle = wx.IconBundle()
        icon_bundle.AddIconFromFile(r"icon\MDC_icon.ico", wx.BITMAP_TYPE_ANY)
        self.SetIcons(icon_bundle)
        #self.SetIcon(icon.MDC_icon.GetIcon())

        menubar = wx.MenuBar()
        self.status_bar = self.CreateStatusBar()

        self.panel = MainPanel(self)

        file_menu = wx.Menu()

        import_menu = wx.Menu()
        iitem = import_menu.Append(wx.ID_ANY, 'Import from a CSV', \
                                              'Import from a CSV')
        self.Bind(wx.EVT_MENU, self.panel.import_csv_file, iitem)

        iitem = import_menu.Append(wx.ID_ANY, 'Import IP list', \
                                              'Import IP list')
        self.Bind(wx.EVT_MENU, self.panel.import_ip_list, iitem)

        iitem = import_menu.Append(wx.ID_ANY, 'Import Plot', 'Import Plot')
        self.Bind(wx.EVT_MENU, self.panel.import_plot, iitem)

        export_menu = wx.Menu()
        eitem = export_menu.Append(wx.ID_ANY, 'Export to a CSV File', \
                                 'Export to a CSV file')
        self.Bind(wx.EVT_MENU, self.panel.export_to_csv, eitem)

        menubar.Append(file_menu, '&File')
        file_menu.AppendMenu(wx.ID_ANY, 'Import', import_menu)
        file_menu.AppendMenu(wx.ID_ANY, 'Export', export_menu)

        fitem = file_menu.Append(wx.ID_EXIT, '&Quit', 'Quit application')
        self.Bind(wx.EVT_MENU, self.on_quit, fitem)

        edit_menu = wx.Menu()

        select_menu = wx.Menu()
        sitem = select_menu.Append(wx.ID_ANY, 'Select All', 'Select All')
        self.Bind(wx.EVT_MENU, self.panel.on_select_all, sitem)

        sitem = select_menu.Append(wx.ID_ANY, 'Select None', 'Select None')
        self.Bind(wx.EVT_MENU, self.panel.on_select_none, sitem)

        menubar.Append(edit_menu, '&Edit')
        edit_menu.AppendMenu(wx.ID_ANY, 'Select', select_menu)

        eitem = edit_menu.Append(wx.ID_ANY, 'Preferences', 'Preferences')
        self.Bind(wx.EVT_MENU, self.panel.configure_prefs, eitem)

        action_menu = wx.Menu()

        aitem = action_menu.Append(wx.ID_ANY, 'Update device information', \
                                   'Update details from selected devices')
        self.Bind(wx.EVT_MENU, self.panel.get_config_info, aitem)

        aitem = action_menu.Append(wx.ID_ANY, 'Configure Device', \
                                   'Configure Devices Connection')
        self.Bind(wx.EVT_MENU, self.panel.configure_device, aitem)

        aitem = action_menu.Append(wx.ID_ANY, 'Send Commands', 'Send Commands')
        self.Bind(wx.EVT_MENU, self.panel.send_commands, aitem)

        aitem = action_menu.Append(wx.ID_ANY, 'Reset Factory', \
                                   'Reset selected devices to factory settings')
        self.Bind(wx.EVT_MENU, self.panel.reset_factory, aitem)

        aitem = action_menu.Append(wx.ID_ANY, 'Reboot Device', \
                                   'Reboot selected devices')
        self.Bind(wx.EVT_MENU, self.panel.reboot, aitem)

        menubar.Append(action_menu, '&Actions')

        tools_menu = wx.Menu()

        titem = tools_menu.Append(wx.ID_ANY, 'Ping devices', 'Ping devices')
        self.Bind(wx.EVT_MENU, self.panel.multi_ping, titem)

        titem = tools_menu.Append(wx.ID_ANY, 'MSE Baseline', 'MSE Baseline')
        self.Bind(wx.EVT_MENU, self.panel.mse_baseline, titem)

        titem = tools_menu.Append(wx.ID_ANY, 'Plot MSE', 'Plot MSE')
        self.Bind(wx.EVT_MENU, self.panel.plot_mse, titem)

        titem = tools_menu.Append(wx.ID_ANY, 'Add a line item', 'Add a line')
        self.Bind(wx.EVT_MENU, self.panel.add_line, titem)

        titem = tools_menu.Append(wx.ID_ANY, 'Generate IP List', \
                                             'Generate IP List')
        self.Bind(wx.EVT_MENU, self.panel.generate_list, titem)

        titem = tools_menu.Append(wx.ID_ANY, 'Generate DGX List', \
                                             'Generate DGX List')
        self.Bind(wx.EVT_MENU, self.panel.generate_DGX_list, titem)

        menubar.Append(tools_menu, 'Tools')

        identify_menu = wx.Menu()

        iitem = identify_menu.Append(wx.ID_ANY, 'Turn on LED\'s', \
                                                'Turn on LED')
        self.Bind(wx.EVT_MENU, self.panel.turn_on_leds, iitem)

        iitem = identify_menu.Append(wx.ID_ANY, 'Turn off LED\'s', \
                                                'Turn off LED')
        self.Bind(wx.EVT_MENU, self.panel.turn_off_leds, iitem)

        menubar.Append(identify_menu, 'Identify')

        listen_menu = wx.Menu()


        self.listen_dhcp = listen_menu.AppendCheckItem(wx.ID_ANY, \
                                                   "Listen for DHCP requests", \
                                                   "Listen for DHCP requests")

        self.Bind(wx.EVT_MENU, self.panel.toggle_dhcp_sniffing, 
                  self.listen_dhcp)
        self.listen_dhcp.Check(self.panel.dhcp_sniffing)

        self.listen_filter = listen_menu.AppendCheckItem(wx.ID_ANY, \
                                           "Filter AMX devices DHCP requests", \
                                           "Filter AMX devices DHCP requests")

        self.Bind(wx.EVT_MENU, self.panel.toggle_filter_amx, self.listen_filter)
        self.listen_filter.Check(self.panel.amx_only_filter)

        menubar.Append(listen_menu, 'Listen')

        delete_menu = wx.Menu()
        ditem = delete_menu.Append(wx.ID_ANY, '&Delete Item', 'Delete Item')
        self.Bind(wx.EVT_MENU, self.panel.delete_item, ditem)

        ditem = delete_menu.Append(wx.ID_ANY, '&Delete All Items', \
                                   'Delete All Items')
        self.Bind(wx.EVT_MENU, self.panel.delete_all_items, ditem)

        menubar.Append(delete_menu, '&Delete')

        help_menu = wx.Menu()
        hitem = help_menu.Append(wx.ID_ANY, 'About', 'About')
        self.Bind(wx.EVT_MENU, self.panel.on_about_box, hitem)

        #hitem = help_menu.Append(wx.ID_ANY, 'Beer', 'Beer')
        #self.Bind(wx.EVT_MENU, self.panel.on_beer_box, hitem)

        menubar.Append(help_menu, '&Help')

        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_CLOSE, self.panel.on_close)

        if self.panel.port_error:
            self.panel.port_errors()

    def on_right_click(self, _):
        """Build a right click menu"""

        rc_menu = wx.Menu()

        rcitem = rc_menu.Append(wx.ID_ANY, 'Update device information')
        self.Bind(wx.EVT_MENU, self.panel.get_config_info, rcitem)

        rcitem = rc_menu.Append(wx.ID_ANY, 'Configure Device')
        self.Bind(wx.EVT_MENU, self.panel.configure_device, rcitem)

        rcitem = rc_menu.Append(wx.ID_ANY, 'Send Commands')
        self.Bind(wx.EVT_MENU, self.panel.send_commands, rcitem)

        rcitem = rc_menu.Append(wx.ID_ANY, 'Reset Factory')
        self.Bind(wx.EVT_MENU, self.panel.reset_factory, rcitem)

        rcitem = rc_menu.Append(wx.ID_ANY, 'Delete')
        self.Bind(wx.EVT_MENU, self.panel.delete_item, rcitem)

        rcitem = rc_menu.Append(wx.ID_ANY, 'Telnet to Device')
        self.Bind(wx.EVT_MENU, self.panel.telnet_to, rcitem)

        rcitem = rc_menu.Append(wx.ID_ANY, 'FactoryAV')
        self.Bind(wx.EVT_MENU, self.panel.factory_av, rcitem)

        rcitem = rc_menu.Append(wx.ID_ANY, 'Reboot Device')
        self.Bind(wx.EVT_MENU, self.panel.reboot, rcitem)

        rcitem = rc_menu.Append(wx.ID_ANY, 'MSE Baseline')
        self.Bind(wx.EVT_MENU, self.panel.mse_baseline, rcitem)

        rcitem = rc_menu.Append(wx.ID_ANY, 'Open device in webbrowser')
        self.Bind(wx.EVT_MENU, self.panel.open_url, rcitem)

        self.PopupMenu(rc_menu)
        rc_menu.Destroy()

    def on_quit(self, _):
        """Save list and close the program"""
        self.panel.dump_pickle()
        self.Close()'''


########################################################################
class GenApp(wx.App):

    #----------------------------------------------------------------------
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)

    #----------------------------------------------------------------------
    def OnInit(self):
        # create frame here
        frame = MainFrame(None)
        frame.Show()
        return True

#----------------------------------------------------------------------
def main():

    app = GenApp()
    app.MainLoop()

# Run the program
if __name__ == "__main__":
    main()
