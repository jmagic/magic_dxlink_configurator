"""Menus for Magic DXLink Configurator"""

import wx
import csv

class PreferencesConfig(wx.Dialog):
    def __init__(self, parent):

        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, 
                             pos=wx.DefaultPosition, size=wx.DefaultSize, 
                             style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        self.parent = parent

        bsizer1 = wx.BoxSizer(wx.VERTICAL)

        bsizer2 = wx.BoxSizer(wx.VERTICAL)

        self.m_statictext1 = wx.StaticText(self, wx.ID_ANY, u"Preferences", 
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_statictext1.Wrap(-1)
        bsizer2.Add(self.m_statictext1, 0, 
                    wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)


        bsizer1.Add(bsizer2, 0, wx.EXPAND, 5)

        bsizer3 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticline1 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition,
                                           wx.DefaultSize, wx.LI_HORIZONTAL)
        bsizer3.Add(self.m_staticline1, 0, wx.ALL|wx.EXPAND, 5)


        bsizer1.Add(bsizer3, 0, wx.EXPAND, 5)

        bsizer4 = wx.BoxSizer(wx.VERTICAL)

        self.m_statictext2 = wx.StaticText(self, wx.ID_ANY, 
                                           u"Master and Device Defaults", 
                                           wx.DefaultPosition, 
                                           wx.DefaultSize, 0)
        self.m_statictext2.Wrap(-1)
        bsizer4.Add(self.m_statictext2, 0, wx.ALL, 5)


        bsizer1.Add(bsizer4, 0, wx.EXPAND, 5)

        bsizer6 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_statictext4 = wx.StaticText(self, wx.ID_ANY, u"Master Address", 
                                         wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_statictext4.Wrap(-1)
        bsizer6.Add(self.m_statictext4, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        self.master_address = wx.TextCtrl(self, wx.ID_ANY, 
                                          self.parent.master_address, 
                                          wx.DefaultPosition, 
                                          wx.DefaultSize, 0)
        bsizer6.Add(self.master_address, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)


        bsizer1.Add(bsizer6, 0, wx.EXPAND, 5)

        bsizer7 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_statictext5 = wx.StaticText(self, wx.ID_ANY, u"Device Number",
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_statictext5.Wrap(-1)
        bsizer7.Add(self.m_statictext5, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        self.device_number = wx.TextCtrl(self, wx.ID_ANY, 
                                         self.parent.device_number, 
                                         wx.DefaultPosition, wx.DefaultSize, 0)
        bsizer7.Add(self.device_number, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)


        bsizer1.Add(bsizer7, 0, wx.EXPAND, 5)

        bsizer8 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticline2 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, 
                                            wx.DefaultSize, wx.LI_HORIZONTAL)
        bsizer8.Add(self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5)


        bsizer1.Add(bsizer8, 0, wx.EXPAND, 5)

        bsizer9 = wx.BoxSizer(wx.VERTICAL)

        self.m_statictext6 = wx.StaticText(self, wx.ID_ANY, u"Notifications",
                                           wx.DefaultPosition, 
                                           wx.DefaultSize, 0)
        self.m_statictext6.Wrap(-1)
        bsizer9.Add(self.m_statictext6, 0, wx.ALL, 5)


        bsizer1.Add(bsizer9, 0, wx.EXPAND, 5)

        bsizer10 = wx.BoxSizer(wx.VERTICAL)

        self.success = wx.CheckBox(self, wx.ID_ANY, 
                                   u"Display Successful Connections", 
                                   wx.DefaultPosition, wx.DefaultSize, 0)
        self.success.SetValue(self.parent.displaysuccess)
        bsizer10.Add(self.success, 0, wx.ALL, 5)

        self.sounds = wx.CheckBox(self, wx.ID_ANY, u"Play Sounds",
                                  wx.DefaultPosition, wx.DefaultSize, 0)
        self.sounds.SetValue(self.parent.play_sounds)
        bsizer10.Add(self.sounds, 0, wx.ALL, 5)

        bsizer1.Add(bsizer10, 0, wx.EXPAND, 5)

        bsizer11 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticline3 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition,
                                           wx.DefaultSize, wx.LI_HORIZONTAL)
        bsizer11.Add(self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5)


        bsizer1.Add(bsizer11, 0, wx.EXPAND, 5)

        bsizer12 = wx.BoxSizer(wx.VERTICAL)

        self.m_statictext7 = wx.StaticText(self, wx.ID_ANY, 
                                           u"Columns To Display", 
                                           wx.DefaultPosition, 
                                           wx.DefaultSize, 0)
        self.m_statictext7.Wrap(-1)
        bsizer12.Add(self.m_statictext7, 0, wx.ALL, 5)


        bsizer1.Add(bsizer12, 0, wx.EXPAND, 5)

        bsizer13 = wx.BoxSizer(wx.HORIZONTAL)

        bsizer22 = wx.BoxSizer(wx.VERTICAL)

        self.display_time = wx.CheckBox(self, wx.ID_ANY, u"Time", 
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        self.display_time.SetValue((int(self.parent.columns_config[0])))
        bsizer22.Add(self.display_time, 0, wx.ALL, 5)


        bsizer13.Add(bsizer22, 1, 0, 5)

        bsizer23 = wx.BoxSizer(wx.VERTICAL)

        self.display_model = wx.CheckBox(self, wx.ID_ANY, u"Model", 
                                         wx.DefaultPosition, wx.DefaultSize, 0)
        self.display_model.SetValue((int(self.parent.columns_config[1])))
        bsizer23.Add(self.display_model, 0, wx.ALL, 5)


        bsizer13.Add(bsizer23, 1, 0, 5)


        bsizer1.Add(bsizer13, 0, wx.EXPAND, 5)

        bsizer14 = wx.BoxSizer(wx.HORIZONTAL)

        bsizer24 = wx.BoxSizer(wx.VERTICAL)

        self.display_mac = wx.CheckBox(self, wx.ID_ANY, u"MAC", 
                                       wx.DefaultPosition, wx.DefaultSize, 0)
        self.display_mac.SetValue((int(self.parent.columns_config[2])))
        bsizer24.Add(self.display_mac, 0, wx.ALL, 5)


        bsizer14.Add(bsizer24, 1, wx.EXPAND, 5)

        bsizer25 = wx.BoxSizer(wx.VERTICAL)

        self.display_ip = wx.CheckBox(self, wx.ID_ANY, u"IP", 
                                      wx.DefaultPosition, wx.DefaultSize, 0)
        self.display_ip.SetValue((int(self.parent.columns_config[3])))
        bsizer25.Add(self.display_ip, 0, wx.ALL, 5)


        bsizer14.Add(bsizer25, 1, wx.EXPAND, 5)


        bsizer1.Add(bsizer14, 0, wx.EXPAND, 5)

        bsizer15 = wx.BoxSizer(wx.HORIZONTAL)

        bsizer26 = wx.BoxSizer(wx.VERTICAL)

        self.display_hostname = wx.CheckBox(self, wx.ID_ANY, u"Hostname",
                                            wx.DefaultPosition, 
                                            wx.DefaultSize, 0)
        self.display_hostname.SetValue((int(self.parent.columns_config[4])))
        bsizer26.Add(self.display_hostname, 0, wx.ALL, 5)


        bsizer15.Add(bsizer26, 1, wx.EXPAND, 5)

        bsizer27 = wx.BoxSizer(wx.VERTICAL)

        self.display_serial = wx.CheckBox(self, wx.ID_ANY, u"Serial Number",
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.display_serial.SetValue((int(self.parent.columns_config[5])))
        bsizer27.Add(self.display_serial, 0, wx.ALL, 5)


        bsizer15.Add(bsizer27, 1, wx.EXPAND, 5)


        bsizer1.Add(bsizer15, 0, wx.EXPAND, 5)

        bsizer16 = wx.BoxSizer(wx.HORIZONTAL)

        bsizer28 = wx.BoxSizer(wx.VERTICAL)

        self.display_firmware = wx.CheckBox(self, wx.ID_ANY, u"Firmware", 
                                            wx.DefaultPosition, 
                                            wx.DefaultSize, 0)
        self.display_firmware.SetValue((int(self.parent.columns_config[6])))
        bsizer28.Add(self.display_firmware, 0, wx.ALL, 5)


        bsizer16.Add(bsizer28, 1, wx.EXPAND, 5)

        bsizer29 = wx.BoxSizer(wx.VERTICAL)

        self.display_device = wx.CheckBox(self, wx.ID_ANY, u"Device",  
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.display_device.SetValue((int(self.parent.columns_config[7])))
        bsizer29.Add(self.display_device, 0, wx.ALL, 5)


        bsizer16.Add(bsizer29, 1, wx.EXPAND, 5)


        bsizer1.Add(bsizer16, 0, wx.EXPAND, 5)

        bsizer17 = wx.BoxSizer(wx.HORIZONTAL)

        bsizer30 = wx.BoxSizer(wx.VERTICAL)

        self.display_static = wx.CheckBox(self, wx.ID_ANY, u"Static",
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.display_static.SetValue((int(self.parent.columns_config[8])))
        bsizer30.Add(self.display_static, 0, wx.ALL, 5)


        bsizer17.Add(bsizer30, 1, wx.EXPAND, 5)

        bsizer31 = wx.BoxSizer(wx.VERTICAL)

        self.display_master = wx.CheckBox(self, wx.ID_ANY, u"Master", 
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.display_master.SetValue((int(self.parent.columns_config[9])))
        bsizer31.Add(self.display_master, 0, wx.ALL, 5)

        bsizer17.Add(bsizer31, 1, wx.EXPAND, 5)

        bsizer1.Add(bsizer17, 0, wx.EXPAND, 5)

        bsizer20 = wx.BoxSizer(wx.HORIZONTAL)

        bsizer32 = wx.BoxSizer(wx.VERTICAL)

        self.display_system = wx.CheckBox(self, wx.ID_ANY, u"System", 
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.display_system.SetValue((int(self.parent.columns_config[10])))
        bsizer32.Add(self.display_system, 0, wx.ALL, 5)


        bsizer20.Add(bsizer32, 1, wx.EXPAND, 5)

        bsizer33 = wx.BoxSizer(wx.VERTICAL)


        bsizer20.Add(bsizer33, 1, wx.EXPAND, 5)


        bsizer1.Add(bsizer20, 0, wx.EXPAND, 5)

        bsizer21 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticline4 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition,
                                           wx.DefaultSize, wx.LI_HORIZONTAL)
        bsizer21.Add(self.m_staticline4, 0, wx.EXPAND |wx.ALL, 5)


        bsizer1.Add(bsizer21, 0, wx.EXPAND, 5)

        bsizer34 = wx.BoxSizer(wx.VERTICAL)

        choice = wx.StdDialogButtonSizer()
        self.choice_ok = wx.Button(self, wx.ID_OK)
        choice.AddButton(self.choice_ok)
        self.choice_cancel = wx.Button(self, wx.ID_CANCEL)
        choice.AddButton(self.choice_cancel)
        choice.Realize()

        bsizer34.Add(choice, 1, wx.EXPAND, 5)


        bsizer1.Add(bsizer34, 0, wx.EXPAND, 5)

        bsizer35 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticline5 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition,
                                           wx.DefaultSize, wx.LI_HORIZONTAL)
        bsizer35.Add(self.m_staticline5, 0, wx.EXPAND |wx.ALL, 5)


        bsizer1.Add(bsizer35, 0, wx.EXPAND, 5)


        self.SetSizer(bsizer1)
        self.Layout()
        bsizer1.Fit(self)

        self.Centre(wx.BOTH)

        # Connect Events
        self.choice_cancel.Bind(wx.EVT_BUTTON, self.on_click)
        self.choice_ok.Bind(wx.EVT_BUTTON, self.on_click)


    def on_click(self, _):
        """When user clicks ok"""
        self.parent.columns_config = (str((int(self.display_time.GetValue()))) +
                               str(int(self.display_model.GetValue())) +
                               str(int(self.display_mac.GetValue())) +
                               str(int(self.display_ip.GetValue())) +
                               str(int(self.display_hostname.GetValue())) +
                               str(int(self.display_serial.GetValue())) +
                               str(int(self.display_firmware.GetValue())) +
                               str(int(self.display_device.GetValue())) +
                               str(int(self.display_static.GetValue())) +
                               str(int(self.display_master.GetValue())) +
                               str(int(self.display_system.GetValue())))

        self.parent.master_address = self.master_address.GetValue()
        self.parent.device_number = self.device_number.GetValue()
        self.parent.displaysuccess = self.success.GetValue()
        self.parent.play_sounds = self.sounds.GetValue()
        self.parent.update_status_bar()
        self.parent.write_config_file()
        self.parent.select_columns()
        self.parent.resize_frame()
        self.Destroy()


class DeviceConfig(wx.Dialog):
    def __init__(self, parent, obj):

        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, 
                            title=wx.EmptyString, 
                            pos=wx.DefaultPosition, 
                            size=wx.DefaultSize, 
                            style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bsizer1 = wx.BoxSizer(wx.VERTICAL)

        bsizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_statictext1 = wx.StaticText(self, wx.ID_ANY, u"Hostname", 
                                           wx.DefaultPosition, 
                                           wx.DefaultSize, 0)
        self.m_statictext1.Wrap(-1)
        bsizer2.Add(self.m_statictext1, 0, wx.ALIGN_CENTER_VERTICAL|
                                           wx.TOP|
                                           wx.BOTTOM|
                                           wx.RIGHT, 5)

        self.hostname_txt = wx.TextCtrl(self, wx.ID_ANY, obj.hostname,
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        self.hostname_txt.SetMinSize(wx.Size(150, -1))

        bsizer2.Add(self.hostname_txt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)


        bsizer1.Add(bsizer2, 0, wx.TOP|
                                wx.RIGHT|
                                wx.LEFT|
                                wx.ALIGN_CENTER_HORIZONTAL, 5)

        bsizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.dhcp_btn = wx.RadioButton(self, wx.ID_ANY, u"DHCP", 
                                       wx.DefaultPosition, wx.DefaultSize, 0)
        bsizer3.Add(self.dhcp_btn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        self.Bind(wx.EVT_RADIOBUTTON, self.on_dhcp, self.dhcp_btn)

        self.static_btn = wx.RadioButton(self, wx.ID_ANY, u"Static", 
                                         wx.DefaultPosition, wx.DefaultSize, 0)
        bsizer3.Add(self.static_btn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        self.Bind(wx.EVT_RADIOBUTTON, self.on_dhcp, self.static_btn)

        bsizer1.Add(bsizer3, 1, wx.ALIGN_RIGHT|wx.RIGHT|wx.LEFT|wx.EXPAND, 5)

        sbsizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"IP info"),
                                     wx.VERTICAL)

        fgsizer2 = wx.FlexGridSizer(3, 2, 0, 0)
        fgsizer2.SetFlexibleDirection(wx.BOTH)
        fgsizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_statictext7 = wx.StaticText(self, wx.ID_ANY, u"IP Address", 
                                           wx.DefaultPosition, 
                                           wx.DefaultSize, 0)
        self.m_statictext7.Wrap(-1)
        fgsizer2.Add(self.m_statictext7, 0, wx.ALL|
                                            wx.ALIGN_CENTER_HORIZONTAL|
                                            wx.ALIGN_CENTER_VERTICAL, 5)

        self.ip_address_txt = wx.TextCtrl(self, wx.ID_ANY, obj.ip_address, 
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.ip_address_txt.SetMinSize(wx.Size(150, -1))

        fgsizer2.Add(self.ip_address_txt, 0, wx.ALIGN_CENTER_VERTICAL|
                                             wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_statictext8 = wx.StaticText(self, wx.ID_ANY, u"Subnet Mask", 
                                           wx.DefaultPosition, 
                                           wx.DefaultSize, 0)
        self.m_statictext8.Wrap(-1)
        fgsizer2.Add(self.m_statictext8, 0, wx.ALL|
                                            wx.ALIGN_CENTER_HORIZONTAL|
                                            wx.ALIGN_CENTER_VERTICAL, 5)

        self.subnet_txt = wx.TextCtrl(self, wx.ID_ANY, obj.subnet, 
                                      wx.DefaultPosition, wx.DefaultSize, 0)
        self.subnet_txt.SetMinSize(wx.Size(150, -1))

        fgsizer2.Add(self.subnet_txt, 1, wx.ALL, 5)

        self.m_statictext9 = wx.StaticText(self, wx.ID_ANY, u"Gateway IP", 
                                           wx.DefaultPosition, 
                                           wx.DefaultSize, 0)
        self.m_statictext9.Wrap(-1)
        fgsizer2.Add(self.m_statictext9, 0, wx.ALL|
                                            wx.ALIGN_CENTER_VERTICAL|
                                            wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.gateway_txt = wx.TextCtrl(self, wx.ID_ANY, obj.gateway, 
                                       wx.DefaultPosition, wx.DefaultSize, 0)
        self.gateway_txt.SetMinSize(wx.Size(150, -1))

        fgsizer2.Add(self.gateway_txt, 0, wx.ALL, 5)


        sbsizer1.Add(fgsizer2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)


        bsizer1.Add(sbsizer1, 0, wx.EXPAND|wx.ALL, 5)

        sbsizer2 = wx.StaticBoxSizer(wx.StaticBox(self, 
                                     wx.ID_ANY, u"Master Info"), wx.VERTICAL)

        fgsizer3 = wx.FlexGridSizer(2, 2, 0, 0)
        fgsizer3.SetFlexibleDirection(wx.BOTH)
        fgsizer3.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_statictext10 = wx.StaticText(self, wx.ID_ANY, u"Master Address", 
                                            wx.DefaultPosition, 
                                            wx.DefaultSize, 0)
        self.m_statictext10.Wrap(-1)
        fgsizer3.Add(self.m_statictext10, 0, wx.ALL|
                                             wx.ALIGN_CENTER_HORIZONTAL|
                                             wx.ALIGN_CENTER_VERTICAL, 5)

        self.master_txt = wx.TextCtrl(self, wx.ID_ANY, obj.master, 
                                      wx.DefaultPosition, wx.DefaultSize, 0)
        self.master_txt.SetMinSize(wx.Size(150, -1))

        fgsizer3.Add(self.master_txt, 0, wx.ALL|
                                         wx.ALIGN_CENTER_HORIZONTAL|
                                         wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_statictext11 = wx.StaticText(self, wx.ID_ANY, u"Device Number",
                                            wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_statictext11.Wrap(-1)
        fgsizer3.Add(self.m_statictext11, 0, wx.ALL|
                                             wx.ALIGN_CENTER_HORIZONTAL|
                                             wx.ALIGN_CENTER_VERTICAL, 5)

        self.device_txt = wx.TextCtrl(self, wx.ID_ANY, obj.device,
                                      wx.DefaultPosition, wx.DefaultSize, 0)
        self.device_txt.SetMinSize(wx.Size(150, -1))

        fgsizer3.Add(self.device_txt, 0, wx.ALL|
                                         wx.ALIGN_CENTER_HORIZONTAL|
                                         wx.ALIGN_CENTER_VERTICAL, 5)


        sbsizer2.Add(fgsizer3, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)


        bsizer1.Add(sbsizer2, 0, wx.ALL|
                                  wx.EXPAND|
                                  wx.ALIGN_CENTER_HORIZONTAL, 5)

        bsizer4 = wx.BoxSizer(wx.HORIZONTAL)

        self.set_btn = wx.Button(self, wx.ID_ANY, u"Set", 
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        bsizer4.Add(self.set_btn, 0, wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.on_set, self.set_btn)

        self.cancel_btn = wx.Button(self, wx.ID_ANY, u"Cancel", 
                                    wx.DefaultPosition, wx.DefaultSize, 0)
        bsizer4.Add(self.cancel_btn, 0, wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.cancel_btn)

        self.abort_btn = wx.Button(self, wx.ID_ANY, u"Abort", 
                                   wx.DefaultPosition, wx.DefaultSize, 0)
        bsizer4.Add(self.abort_btn, 0, wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.on_abort, self.abort_btn)


        bsizer1.Add(bsizer4, 0, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5)


        self.SetSizer(bsizer1)
        self.Layout()
        bsizer1.Fit(self)

        self.Centre(wx.BOTH)

        self.parent = parent
        self.obj = obj
        self.ip_org = obj.ip_address

        self.SetTitle("Device settings for %s %s" %(obj.ip_address, obj.device))
        self.hostname = obj.hostname
        self.ip_address = obj.ip_address
        self.subnet = obj.subnet
        self.gateway = obj.gateway
        self.master = obj.master
        self.device = obj.device

        if self.hostname == ' ':
            self.hostname = 'hostname'
        if self.ip_address == ' ':
            self.ip_address = '0.0.0.0'
        if self.subnet == ' ':
            self.subnet = '255.255.255.0'
        if self.gateway == ' ':
            self.gateway = '0.0.0.0'
        if self.master == ' ' or self.master == 'not connected':
            self.master = str(self.parent.master_address)
            self.master_txt.SetValue(self.parent.master_address)
        if self.device == ' ' or obj.device == '0':
            self.device = str(self.parent.device_number)
            self.device_txt.SetValue(self.parent.device_number)

        if obj.ip_type == 's':
            self.dhcp_btn.SetValue(False)
            self.static_btn.SetValue(True)
        else:
            self.dhcp_btn.SetValue(True)
            self.static_btn.SetValue(False)

        self.on_dhcp(None) #call to update dhcp / static

    def on_dhcp(self, _):
        """Sets DHCP mode on or off and enables the DHCP options"""

        if self.dhcp_btn.GetValue() == True:
            self.ip_address_txt.Enable(False)
            self.subnet_txt.Enable(False)
            self.gateway_txt.Enable(False)

        else:
            self.ip_address_txt.Enable(True)
            self.subnet_txt.Enable(True)
            self.gateway_txt.Enable(True)


    def on_cancel(self, _):
        """Canel and close"""
        self.Destroy()

    def on_abort(self, _):
        """Quits processing the list of selected items"""
        self.parent.abort = True
        self.Destroy()

    def on_set(self, _):
        """Sends the setting to the device"""
        if self.dhcp_btn.GetValue() == True:
            setdhcp = True
        else:
            setdhcp = False

        info = ['DeviceConfig',
                self.obj,
                self.parent.telnet_timeout_seconds,
                setdhcp, str(self.hostname_txt.GetValue()),
                str(self.ip_org),
                str(self.ip_address_txt.GetValue()),
                str(self.subnet_txt.GetValue()),
                str(self.gateway_txt.GetValue()),
                str(self.master_txt.GetValue()),
                str(self.device_txt.GetValue())]

        #self.parent.static_items.append(self.obj)
        self.parent.telnet_job_queue.put(info)
        self.parent.display_progress()
        self.Destroy()


class IpListGen(wx.Dialog):
    def __init__(self, parent):

        wx.Dialog.__init__(self, parent=parent, id=wx.ID_ANY)

        self.parent = parent

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bsizer1 = wx.BoxSizer(wx.VERTICAL)

        bsizer2 = wx.BoxSizer(wx.HORIZONTAL)

        bsizer5 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_statictext1 = wx.StaticText(self, wx.ID_ANY, u"Starting IP", 
                                           wx.DefaultPosition, 
                                           wx.DefaultSize, 0)
        self.m_statictext1.Wrap(-1)
        bsizer5.Add(self.m_statictext1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)


        bsizer2.Add(bsizer5, 0, wx.EXPAND, 5)

        bsizer6 = wx.BoxSizer(wx.VERTICAL)

        self.start_ip = wx.TextCtrl(self, wx.ID_ANY, self.parent.master_address,
                                    wx.DefaultPosition, wx.DefaultSize, 0)
        bsizer6.Add(self.start_ip, 0, wx.ALL|wx.EXPAND, 5)


        bsizer2.Add(bsizer6, 1, wx.EXPAND, 5)


        bsizer1.Add(bsizer2, 0, wx.EXPAND, 5)

        bsizer3 = wx.BoxSizer(wx.HORIZONTAL)

        bsizer7 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_statictext2 = wx.StaticText(self, wx.ID_ANY, u"Finishing IP",
                                           wx.DefaultPosition, 
                                           wx.DefaultSize, 0)
        self.m_statictext2.Wrap(-1)
        bsizer7.Add(self.m_statictext2, 0, wx.ALL, 5)


        bsizer3.Add(bsizer7, 0, wx.ALIGN_CENTER_VERTICAL, 5)

        bsizer8 = wx.BoxSizer(wx.VERTICAL)

        self.finish_ip = wx.TextCtrl(self, wx.ID_ANY, 
                                     self.parent.master_address, 
                                     wx.DefaultPosition, wx.DefaultSize, 0)
        bsizer8.Add(self.finish_ip, 1, wx.ALL|wx.EXPAND, 5)


        bsizer3.Add(bsizer8, 1, wx.EXPAND, 5)


        bsizer1.Add(bsizer3, 0, wx.EXPAND, 5)

        bsizer4 = wx.BoxSizer(wx.VERTICAL)

        bsizer9 = wx.BoxSizer(wx.HORIZONTAL)

        self.replace = wx.Button(self, wx.ID_ANY, u"Replace List", 
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        bsizer9.Add(self.replace, 0, wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.on_replace, self.replace)

        self.add = wx.Button(self, wx.ID_ANY, u"Add to List", 
                             wx.DefaultPosition, wx.DefaultSize, 0)
        bsizer9.Add(self.add, 0, wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.on_add, self.add)

        self.save = wx.Button(self, wx.ID_ANY, u"Save as File", 
                              wx.DefaultPosition, wx.DefaultSize, 0)
        bsizer9.Add(self.save, 0, wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.on_save, self.save)


        bsizer4.Add(bsizer9, 1, wx.EXPAND, 5)


        bsizer1.Add(bsizer4, 1, wx.EXPAND, 5)


        self.SetSizer(bsizer1)
        self.Layout()
        bsizer1.Fit(self)

        self.Centre(wx.BOTH)

        self.data = []

        self.SetTitle("Generate IP list")


    def on_replace(self, _):
        """Replaces list with generated list"""
        self.parent.main_list.DeleteAllItems()
        self.on_add(None)

    def on_add(self, _):
        """Adds to the bottom of the list"""
        self.gen_list()
        for item in self.data:
            self.parent.main_list.AddObject(self.parent.makeUnit(
                                            ('', '', str(item))))
        self.parent.dumpPickle()
        self.Destroy()

    def on_save(self, _):
        """Saves the ip list to a file"""
        self.gen_list()
        save_file_dialog = wx.FileDialog(self, message="Save IP list",
                                         defaultDir=self.parent.path,
                                         defaultFile="generatediplist.csv",
                                         wildcard="CSV files (*.csv)|*.csv",
                                         style=wx.SAVE)
        if save_file_dialog.ShowModal() == wx.ID_OK:

            path = save_file_dialog.GetPath()
            with open(path, 'wb') as ip_list_file:
                writer_csv = csv.writer(ip_list_file)
                for item in self.data:
                    writer_csv.writerow([item])
                self.Destroy()
        else:
            self.Destroy()

    def gen_list(self):
        """Generates the IP list"""
        self.data = []
        count = 0
        #try: Later
        start = str(self.start_ip.GetValue())
        start = start.split('.')[3]
        finish = str(self.finish_ip.GetValue())
        finish = finish.split('.')[3]
        for _ in range(int(start), (int(finish)+1)):
            ip_gen = (self.start_ip.GetValue().split('.')[0] + "." +
                      self.start_ip.GetValue().split('.')[1] + "." +
                      self.start_ip.GetValue().split('.')[2] + "." +
                      str(int(start)  + count))
            self.data.append(ip_gen)
            count += 1

