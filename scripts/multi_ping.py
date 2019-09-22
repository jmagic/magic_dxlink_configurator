"""Continuously pings devices for troubleshooting"""

import wx
import os
from ObjectListView import FastObjectListView as ObjectListView, ColumnDefn
from . import mdc_gui
from pydispatch import dispatcher


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
    def __init__(self, parent):
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
        self.log_path = os.path.join(self.parent.path, 'ping_logs')
        self.log_path_txt.SetLabel(self.log_path)

        self.SetTitle("Multiple Ping Monitor")
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_refresh, self.redraw_timer)
        self.redraw_timer.Start(1000)

        dispatcher.connect(self.list_update,
                           signal='Ping Model Update',
                           sender=dispatcher.Any)

    def list_update(self, sender):
        # print 'in list update: ', sender
        self.ping_list.SetObjects(sender)

    def on_refresh(self, event):
        """ Refreshes the display """
        self.ping_list.RefreshObjects(self.ping_list.GetObjects())

    def on_delete(self, event):
        """Removes an item from pinging"""
        for obj in self.ping_list.GetSelectedObjects():
            self.parent.multi_ping_remove(obj)
        self.ping_list.RemoveObjects(self.ping_list.GetSelectedObjects())

    def on_redraw_timer(self, _):
        """Refresh objects when timer expires"""
        if len(self.parent.ping_model.ping_objects) != len(self.ping_list.GetObjects()):
            print('list has changed')
            self.list_update(self.parent.ping_model.ping_objects)
        self.ping_list.RefreshObjects()

    def on_reset(self, _):
        """Resets the selected item"""
        for obj in self.ping_list.GetSelectedObjects():
            obj.ping_data = []
            obj.success = 0
            obj.failed = 0
            self.ping_list.RefreshObject(obj)

    def on_log_enable(self, _):
        """Turns logging on"""
        self.parent.multi_ping_logging()

    def on_close(self, event):
        """Close the window"""
        self.Hide()
        self.parent.multi_ping_shutdown()
        # self.Destroy()
        event.Skip()

    def on_show_details(self, _):
        """Show the details of the pings to this device"""
        for obj in self.ping_list.GetSelectedObjects():
            dia = PingDetail(self, obj)
            dia.Show()
