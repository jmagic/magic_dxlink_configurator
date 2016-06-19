"""Continuously pings devices for troubleshooting"""

import wx
from pydispatch import dispatcher
from ObjectListView import ObjectListView, ColumnDefn
import datetime
import csv
import os
import time
import mdc_gui
import ping_class


class PingUnit(object):
    """
    Model of the Ping Unit

    Contains the following attributes:
    'hostname','serial','device','mac',
    """
    # ----------------------------------------------------------------------
    def __init__(self, ping_data, hostname, serial, ip_address, mac_address):

        self.ping_data = ping_data
        self.hostname = hostname
        self.serial = serial
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.success = 0
        self.failed = 0


class Ping_Data_Unit(object):
    """
    Model of the Ping_Data_Unit

    Contains the following attributes:
    ping_time, ms delay, successful """
    # ----------------------------------------------------------------------
    def __init__(self, ping_time, ms_delay, success):

        self.ping_time = ping_time
        self.ms_delay = ms_delay
        self.success = success


class PingDetail(mdc_gui.PingDetail):
    def __init__(self, parent, device_object):
        mdc_gui.PingDetail.__init__(self, parent)

        self.detail_list = ObjectListView(self.olv_panel, wx.ID_ANY,
                                          style=wx.LC_REPORT |
                                          wx.SUNKEN_BORDER)

        self.detail_list.SetColumns(
            [ColumnDefn("Time", "center", 180, "ping_time",
                        stringConverter="%d-%m-%Y %H:%M:%S.%f"),
             ColumnDefn("ms Delay", "center", 80, "ms_delay"),
             ColumnDefn("Success", "center", 80, "success")])
        self.olv_sizer.Add(self.detail_list, 1, wx.ALL | wx.EXPAND, 0)
        self.olv_sizer.Layout()
        self.SetTitle("Details View for " + device_object.ip_address)
        self.device_object = device_object
        self.detail_list.SetObjects(device_object.ping_data)

        self.auto_update = self.auto_update_chk.GetValue()
        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_refresh, self.redraw_timer)
        if self.auto_update:
            self.redraw_timer.Start(1000)

    def on_refresh(self, _):
        self.detail_list.SetObjects(self.device_object.ping_data)
        self.detail_list.SelectObject(self.detail_list.GetObjects()[-1], ensureVisible=True)

    def on_auto_update(self, _):
        self.auto_update = not self.auto_update
        self.auto_update_chk.SetValue(self.auto_update)
        if self.auto_update:
            self.redraw_timer.Start(1000)
        else:
            self.redraw_timer.Stop()


class DetailsView(wx.Dialog):

    def __init__(self, parent, device_object):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString,
                           pos=wx.DefaultPosition, size=wx.Size(400, 550),
                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bsizer1 = wx.BoxSizer(wx.VERTICAL)

        bsizer121 = wx.BoxSizer(wx.VERTICAL)

        self.ping_list = ObjectListView(self, wx.ID_ANY, size=wx.Size(-1, 500),
                                        style=wx.LC_REPORT |
                                        wx.SUNKEN_BORDER |
                                        wx.RESIZE_BORDER)
        self.ping_list.SetColumns(
            [ColumnDefn("Time", "center", 180, "ping_time",
                        stringConverter="%d-%m-%Y %H:%M:%S.%f"),
             ColumnDefn("ms Delay", "center", 80, "ms_delay"),
             ColumnDefn("Success", "center", 80, "success")])

        bsizer121.Add(self.ping_list, 1, wx.ALL | wx.EXPAND, 5)
        bsizer1.Add(bsizer121, 0, wx.EXPAND, 5)

        self.SetSizer(bsizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # ------------------------------ Done with wxFormBuilder

        self.parent = parent
        self.SetTitle("Details View for " + device_object.ip_address)
        self.ping_list.SetObjects(device_object.ping_data)


class MultiPing(mdc_gui.MultiPing):
    def __init__(self, parent, device_list):
        mdc_gui.MultiPing.__init__(self, parent)

        self.ping_list = ObjectListView(self.olv_panel, wx.ID_ANY,
                                        style=wx.LC_REPORT |
                                        wx.SUNKEN_BORDER)
        self.ping_list.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,
                            self.MultiPingOnContextMenu)
        self.ping_list.SetColumns(
            [ColumnDefn("IP", "center", 100, "ip_address"),
             ColumnDefn("MAC", "center", 130, "mac_address"),
             ColumnDefn("Hostname", "center", 130, "hostname"),
             ColumnDefn("Serial", "center", 150, "serial"),
             ColumnDefn("Successful Pings", "center", 110, "success"),
             ColumnDefn("Failed Pings", "center", 80, "failed")])

        self.olv_sizer.Add(self.ping_list, 1, wx.ALL | wx.EXPAND, 0)
        self.olv_sizer.Layout()

        self.parent = parent
        self.SetTitle("Multiple Ping Monitor")
        self.ping_objects = self.set_objects(device_list)
        self.ping_list.SetObjects(self.ping_objects)
        self.log_files = {}
        self.log_link_txt.SetURL(os.path.join(self.parent.path, 'ping_logs'))
        self.logging = False
        self.on_log_enable(None)
        self.ping_threads = []

        for obj in device_list:
            ping_thread = ping_class.PingJob(self, obj)
            ping_thread.setDaemon(True)
            ping_thread.start()
            self.ping_threads.append(ping_thread)
            # self.parent.telnet_job_queue.put(
            #     ['ping', obj, self.parent.telnet_timeout_seconds])

        for obj in self.ping_objects:
            self.log_files[obj] = (
                'device_' +
                obj.ip_address +
                '_time_' +
                datetime.datetime.now().strftime('%H_%M_%S') +
                '.csv')

        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_refresh, self.redraw_timer)
        self.redraw_timer.Start(1000)
        dispatcher.connect(
            self.on_incoming_ping,
            signal="Incoming Ping",
            sender=dispatcher.Any)

    def on_refresh(self, event):
        """ Refreshes the display """
        self.ping_list.RefreshObjects(self.ping_list.GetObjects())

    def add_items(self, objs):
        new_objs = self.set_objects(objs)

        for obj in new_objs:
            for item in self.ping_objects:
                if item.ip_address == obj.ip_address:
                    return
            self.ping_objects.append(obj)
            self.parent.telnet_job_queue.put(
                ['ping', obj, self.parent.telnet_timeout_seconds])

            self.log_files[obj] = (
                'device_' +
                obj.ip_address +
                '_time_' +
                datetime.datetime.now().strftime('%H_%M_%S') +
                '.csv')
        self.ping_list.SetObjects(self.ping_objects)

    def on_delete(self, event):
        """Removes an item from pinging"""
        for obj in self.ping_list.GetSelectedObjects():
            for item in self.ping_threads:
                if item.obj.ip_address == obj.ip_address:
                    item.keeprunning = False
            self.log_files.pop(obj, None)
            self.ping_objects.remove(obj)
        self.ping_list.RemoveObjects(self.ping_list.GetSelectedObjects())

    def on_redraw_timer(self, _):
        """Refresh objects when timer expires"""
        self.ping_list.RefreshObject(self.ping_objects)

    def on_reset(self, _):
        """Resets the selected item"""
        for obj in self.ping_list.GetSelectedObjects():
            obj.ping_data = []
            obj.success = 0
            obj.failed = 0
            self.ping_list.RefreshObject(obj)

    def set_objects(self, device_list):
        """Creates a ping object and adds it to the list"""
        new_objs = []
        for obj in device_list:

            data = PingUnit(
                [],
                obj.hostname,
                obj.serial,
                obj.ip_address,
                obj.mac_address)
            new_objs.append(data)
        return new_objs

    def set_ping_data(self, ping_info):
        """Makes a ping data unit"""
        return Ping_Data_Unit(
            ping_info[0],  # .strftime('%H:%M:%S.%f')
            ping_info[1],
            ping_info[2])

    def on_log_enable(self, event):
        """Toggles log enable"""
        if self.log_enable_chk.GetValue():
            # self.log_file_txt.SetLabel(
            #     'Logging to: ' +
            #     self.parent.path + 'ping_logs\\'
            #     'device_***IP of device***_' +
            #     time.strftime('%d-%b-%Y-%H-%M-%S') +
            #     '.txt')
            self.logging = True
        else:
            # self.log_file_txt.SetLabel('')
            self.logging = False

    def on_incoming_ping(self, sender):
        """Process an incoming ping"""
        # switch to true to log pings
        # print sender
        # print '.'
        if self.parent.ping_active:
            # for item in sender:
            # print 'start incoming'
            # print sender[0]
            # print sender[0].ip
            for obj in self.ping_objects:

                if sender[0].ip_address == obj.ip_address:

                    obj.ping_data.append(self.set_ping_data(sender[1]))

                    if sender[1][2] == 'Yes':
                        obj.success += 1
                    else:
                        obj.failed += 1
                    # print 'success', str(obj.success)
                    # print 'finish incoming'
                    # self.ping_list.RefreshObject(obj)
                    if self.logging:
                        self.save_log(obj)

    def on_close(self, _):
        """Close the window"""
        self.parent.ping_active = False
        self.Hide()
        self.parent.ping_window = None
        self.Destroy()

    def on_show_details(self, _):
        """Show the details of the pings to this device"""
        for obj in self.ping_list.GetSelectedObjects():
            dia = PingDetail(self, obj)
            dia.Show()

    def save_log(self, obj):
        """Save log to a file"""
        log_path = os.path.join(self.parent.path, 'ping_logs')
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        output_file = os.path.join(log_path, self.log_files[obj])

        with open(output_file, 'ab') as log_file:
            writer_csv = csv.writer(log_file, quoting=csv.QUOTE_ALL)
            row = []
            row.append(str(obj.ping_data[-1].ping_time))
            row.append(str(obj.ping_data[-1].ms_delay))
            row.append(str(obj.ping_data[-1].success))
            writer_csv.writerow(row)
