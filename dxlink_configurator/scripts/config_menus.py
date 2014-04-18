import wx
import datetime
import csv
from pydispatch import dispatcher

class PreferencesConfig(wx.Dialog):
    def __init__(self, parent):

        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        self.parent = parent

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Preferences", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer2.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )

        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer3.Add( self.m_staticline1, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer1.Add( bSizer3, 0, wx.EXPAND, 5 )

        bSizer4 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Master and Device Defaults", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        bSizer4.Add( self.m_staticText2, 0, wx.ALL, 5 )


        bSizer1.Add( bSizer4, 0, wx.EXPAND, 5 )

        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Master Address", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        bSizer6.Add( self.m_staticText4, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.master_address = wx.TextCtrl( self, wx.ID_ANY, self.parent.master_address, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.master_address, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer1.Add( bSizer6, 0, wx.EXPAND, 5 )

        bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Device Number", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )
        bSizer7.Add( self.m_staticText5, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.device_number = wx.TextCtrl( self, wx.ID_ANY, self.parent.device_number, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7.Add( self.device_number, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer1.Add( bSizer7, 0, wx.EXPAND, 5 )

        bSizer8 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer8.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )


        bSizer1.Add( bSizer8, 0, wx.EXPAND, 5 )

        bSizer9 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Notifications", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )
        bSizer9.Add( self.m_staticText6, 0, wx.ALL, 5 )


        bSizer1.Add( bSizer9, 0, wx.EXPAND, 5 )

        bSizer10 = wx.BoxSizer( wx.VERTICAL )

        self.success = wx.CheckBox( self, wx.ID_ANY, u"Display Successful Connections", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.success.SetValue( self.parent.displaysuccess )
        bSizer10.Add( self.success, 0, wx.ALL, 5 )

        self.sounds = wx.CheckBox( self, wx.ID_ANY, u"Play Sounds", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.sounds.SetValue( self.parent.play_sounds )
        bSizer10.Add( self.sounds, 0, wx.ALL, 5 )

        bSizer1.Add( bSizer10, 0, wx.EXPAND, 5 )

        bSizer11 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticline3 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer11.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )


        bSizer1.Add( bSizer11, 0, wx.EXPAND, 5 )

        bSizer12 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Columns To Display", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )
        bSizer12.Add( self.m_staticText7, 0, wx.ALL, 5 )


        bSizer1.Add( bSizer12, 0, wx.EXPAND, 5 )

        bSizer13 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer22 = wx.BoxSizer( wx.VERTICAL )

        self.display_time = wx.CheckBox( self, wx.ID_ANY, u"Time", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.display_time.SetValue((int(self.parent.columns_config[0])))
        bSizer22.Add( self.display_time, 0, wx.ALL, 5 )


        bSizer13.Add( bSizer22, 1, 0, 5 )

        bSizer23 = wx.BoxSizer( wx.VERTICAL )

        self.display_model = wx.CheckBox( self, wx.ID_ANY, u"Model", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.display_model.SetValue((int(self.parent.columns_config[1])))
        bSizer23.Add( self.display_model, 0, wx.ALL, 5 )


        bSizer13.Add( bSizer23, 1, 0, 5 )


        bSizer1.Add( bSizer13, 0, wx.EXPAND, 5 )

        bSizer14 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer24 = wx.BoxSizer( wx.VERTICAL )

        self.display_mac = wx.CheckBox( self, wx.ID_ANY, u"MAC", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.display_mac.SetValue((int(self.parent.columns_config[2])))
        bSizer24.Add( self.display_mac, 0, wx.ALL, 5 )


        bSizer14.Add( bSizer24, 1, wx.EXPAND, 5 )

        bSizer25 = wx.BoxSizer( wx.VERTICAL )

        self.display_ip = wx.CheckBox( self, wx.ID_ANY, u"IP", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.display_ip.SetValue((int(self.parent.columns_config[3])))
        bSizer25.Add( self.display_ip, 0, wx.ALL, 5 )


        bSizer14.Add( bSizer25, 1, wx.EXPAND, 5 )


        bSizer1.Add( bSizer14, 0, wx.EXPAND, 5 )

        bSizer15 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer26 = wx.BoxSizer( wx.VERTICAL )

        self.display_hostname = wx.CheckBox( self, wx.ID_ANY, u"Hostname", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.display_hostname.SetValue((int(self.parent.columns_config[4])))
        bSizer26.Add( self.display_hostname, 0, wx.ALL, 5 )


        bSizer15.Add( bSizer26, 1, wx.EXPAND, 5 )

        bSizer27 = wx.BoxSizer( wx.VERTICAL )

        self.display_serial = wx.CheckBox( self, wx.ID_ANY, u"Serial Number", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.display_serial.SetValue((int(self.parent.columns_config[5])))
        bSizer27.Add( self.display_serial, 0, wx.ALL, 5 )


        bSizer15.Add( bSizer27, 1, wx.EXPAND, 5 )


        bSizer1.Add( bSizer15, 0, wx.EXPAND, 5 )

        bSizer16 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer28 = wx.BoxSizer( wx.VERTICAL )

        self.display_firmware = wx.CheckBox( self, wx.ID_ANY, u"Firmware", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.display_firmware.SetValue((int(self.parent.columns_config[6])))
        bSizer28.Add( self.display_firmware, 0, wx.ALL, 5 )


        bSizer16.Add( bSizer28, 1, wx.EXPAND, 5 )

        bSizer29 = wx.BoxSizer( wx.VERTICAL )

        self.display_device = wx.CheckBox( self, wx.ID_ANY, u"Device", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.display_device.SetValue((int(self.parent.columns_config[7])))
        bSizer29.Add( self.display_device, 0, wx.ALL, 5 )


        bSizer16.Add( bSizer29, 1, wx.EXPAND, 5 )


        bSizer1.Add( bSizer16, 0, wx.EXPAND, 5 )

        bSizer17 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer30 = wx.BoxSizer( wx.VERTICAL )

        self.display_static = wx.CheckBox( self, wx.ID_ANY, u"Static", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.display_static.SetValue((int(self.parent.columns_config[8])))
        bSizer30.Add( self.display_static, 0, wx.ALL, 5 )


        bSizer17.Add( bSizer30, 1, wx.EXPAND, 5 )

        bSizer31 = wx.BoxSizer( wx.VERTICAL )

        self.display_master = wx.CheckBox( self, wx.ID_ANY, u"Master", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.display_master.SetValue((int(self.parent.columns_config[9])))
        bSizer31.Add( self.display_master, 0, wx.ALL, 5 )


        bSizer17.Add( bSizer31, 1, wx.EXPAND, 5 )


        bSizer1.Add( bSizer17, 0, wx.EXPAND, 5 )

        bSizer20 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer32 = wx.BoxSizer( wx.VERTICAL )

        self.display_system = wx.CheckBox( self, wx.ID_ANY, u"System", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.display_system.SetValue((int(self.parent.columns_config[10])))
        bSizer32.Add( self.display_system, 0, wx.ALL, 5 )


        bSizer20.Add( bSizer32, 1, wx.EXPAND, 5 )

        bSizer33 = wx.BoxSizer( wx.VERTICAL )


        bSizer20.Add( bSizer33, 1, wx.EXPAND, 5 )


        bSizer1.Add( bSizer20, 0, wx.EXPAND, 5 )

        bSizer21 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticline4 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer21.Add( self.m_staticline4, 0, wx.EXPAND |wx.ALL, 5 )


        bSizer1.Add( bSizer21, 0, wx.EXPAND, 5 )

        bSizer34 = wx.BoxSizer( wx.VERTICAL )

        choice = wx.StdDialogButtonSizer()
        self.choiceOK = wx.Button( self, wx.ID_OK )
        choice.AddButton( self.choiceOK )
        self.choiceCancel = wx.Button( self, wx.ID_CANCEL )
        choice.AddButton( self.choiceCancel )
        choice.Realize();

        bSizer34.Add( choice, 1, wx.EXPAND, 5 )


        bSizer1.Add( bSizer34, 0, wx.EXPAND, 5 )

        bSizer35 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticline5 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer35.Add( self.m_staticline5, 0, wx.EXPAND |wx.ALL, 5 )


        bSizer1.Add( bSizer35, 0, wx.EXPAND, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()
        bSizer1.Fit( self )

        self.Centre( wx.BOTH )

        # Connect Events
        self.choiceCancel.Bind( wx.EVT_BUTTON, self.onClick )
        self.choiceOK.Bind( wx.EVT_BUTTON, self.onClick )


    def onClick( self, event ):
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
        self.parent.updateStatusBar()
        self.parent.writeConfigFile()
        self.parent.selectColumns()
        self.parent.resizeFrame()
        self.Destroy()


class DeviceConfig(wx.Dialog):
    def __init__(self, parent, obj):

        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Hostname", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer2.Add( self.m_staticText1, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.RIGHT, 5 )

        self.hostname_txt = wx.TextCtrl( self, wx.ID_ANY, obj.hostname, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.hostname_txt.SetMinSize( wx.Size( 150,-1 ) )

        bSizer2.Add( self.hostname_txt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer1.Add( bSizer2, 0, wx.TOP|wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

        self.dhcp_btn = wx.RadioButton( self, wx.ID_ANY, u"DHCP", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer3.Add( self.dhcp_btn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        self.Bind(wx.EVT_RADIOBUTTON, self.OnDhcp, self.dhcp_btn)

        self.static_btn = wx.RadioButton( self, wx.ID_ANY, u"Static", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer3.Add( self.static_btn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        self.Bind(wx.EVT_RADIOBUTTON, self.OnDhcp, self.static_btn)

        bSizer1.Add( bSizer3, 1, wx.ALIGN_RIGHT|wx.RIGHT|wx.LEFT|wx.EXPAND, 5 )

        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"IP info" ), wx.VERTICAL )

        fgSizer2 = wx.FlexGridSizer( 3, 2, 0, 0 )
        fgSizer2.SetFlexibleDirection( wx.BOTH )
        fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"IP Address", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )
        fgSizer2.Add( self.m_staticText7, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.ip_address_txt = wx.TextCtrl( self, wx.ID_ANY, obj.ip, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ip_address_txt.SetMinSize( wx.Size( 150,-1 ) )

        fgSizer2.Add( self.ip_address_txt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Subnet Mask", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )
        fgSizer2.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.subnet_txt = wx.TextCtrl( self, wx.ID_ANY, obj.subnet, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.subnet_txt.SetMinSize( wx.Size( 150,-1 ) )

        fgSizer2.Add( self.subnet_txt, 1, wx.ALL, 5 )

        self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"Gateway IP", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )
        fgSizer2.Add( self.m_staticText9, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.gateway_txt = wx.TextCtrl( self, wx.ID_ANY, obj.gateway, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.gateway_txt.SetMinSize( wx.Size( 150,-1 ) )

        fgSizer2.Add( self.gateway_txt, 0, wx.ALL, 5 )


        sbSizer1.Add( fgSizer2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        bSizer1.Add( sbSizer1, 0, wx.EXPAND|wx.ALL, 5 )

        sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Master Info" ), wx.VERTICAL )

        fgSizer3 = wx.FlexGridSizer( 2, 2, 0, 0 )
        fgSizer3.SetFlexibleDirection( wx.BOTH )
        fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"Master Address", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )
        fgSizer3.Add( self.m_staticText10, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.master_txt = wx.TextCtrl( self, wx.ID_ANY, obj.master, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.master_txt.SetMinSize( wx.Size( 150,-1 ) )

        fgSizer3.Add( self.master_txt, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"Device Number", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( -1 )
        fgSizer3.Add( self.m_staticText11, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.device_txt = wx.TextCtrl( self, wx.ID_ANY, obj.device, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.device_txt.SetMinSize( wx.Size( 150,-1 ) )

        fgSizer3.Add( self.device_txt, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )


        sbSizer2.Add( fgSizer3, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )


        bSizer1.Add( sbSizer2, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

        self.set_btn = wx.Button( self, wx.ID_ANY, u"Set", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer4.Add( self.set_btn, 0, wx.ALL, 5 )
        self.Bind(wx.EVT_BUTTON, self.OnSet, self.set_btn)

        self.cancel_btn = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer4.Add( self.cancel_btn, 0, wx.ALL, 5 )
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancel_btn)

        self.abort_btn = wx.Button( self, wx.ID_ANY, u"Abort", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer4.Add( self.abort_btn, 0, wx.ALL, 5 )
        self.Bind(wx.EVT_BUTTON, self.OnAbort, self.abort_btn)


        bSizer1.Add( bSizer4, 0, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()
        bSizer1.Fit( self )

        self.Centre( wx.BOTH )

        '''def __init__(self, parent, obj):

        wx.Dialog.__init__(self, parent=parent, id=wx.ID_ANY)'''


        self.parent = parent
        self.obj = obj
        self.ip_org = obj.ip

        self.SetTitle("Device settings for %s %s" %(obj.ip, obj.device))
        self.hostname = obj.hostname
        self.ip = obj.ip
        self.subnet = obj.subnet
        self.gateway = obj.gateway
        self.master = obj.master
        self.device = obj.device

        if self.hostname == ' ':
            self.hostname = 'hostname'
        if self.ip == ' ':
            self.ip = '0.0.0.0'
        if self.subnet == ' ':
            self.subnet = '255.255.255.0'
        if self.gateway == ' ':
            self.gateway = '0.0.0.0'
        if self.master == ' ' or self.master == 'not connected':
            self.master = str(self.parent.master_address)
            self.master_txt.SetValue(self.parent.master_address)
        if self.device == ' ' or obj.device == '0' :
            self.device = str(self.parent.device_number)
            self.device_txt.SetValue(self.parent.device_number)

        if obj.ip_type == 's':
            self.dhcp_btn.SetValue(False)
            self.static_btn.SetValue(True)
        else:
            self.dhcp_btn.SetValue(True)
            self.static_btn.SetValue(False)

        self.OnDhcp() #call to update dhcp / static

    def OnDhcp(self, data=None):

        if self.dhcp_btn.GetValue() == True:
            self.ip_address_txt.Enable(False)
            self.subnet_txt.Enable(False)
            self.gateway_txt.Enable(False)

        else:
            self.ip_address_txt.Enable(True)
            self.subnet_txt.Enable(True)
            self.gateway_txt.Enable(True)


    def OnCancel(self, event):

        self.Destroy()

    def OnAbort(self, event):

        self.parent.abort = True
        self.Destroy()

    def OnSet(self, event):
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
                str(self.device_txt.GetValue()) ]

        self.parent.staticItems.append(self.obj)
        self.parent.telnetjobqueue.put(info)
        self.Destroy()


class IpListGen(wx.Dialog):
    def __init__(self, parent):

        wx.Dialog.__init__(self, parent=parent, id=wx.ID_ANY)

        self.parent = parent

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Starting IP", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer5.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer2.Add( bSizer5, 0, wx.EXPAND, 5 )

        bSizer6 = wx.BoxSizer( wx.VERTICAL )

        self.start_ip = wx.TextCtrl( self, wx.ID_ANY, self.parent.master_address, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.start_ip, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer2.Add( bSizer6, 1, wx.EXPAND, 5 )


        bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )

        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Finishing IP", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        bSizer7.Add( self.m_staticText2, 0, wx.ALL, 5 )


        bSizer3.Add( bSizer7, 0, wx.ALIGN_CENTER_VERTICAL, 5 )

        bSizer8 = wx.BoxSizer( wx.VERTICAL )

        self.finish_ip = wx.TextCtrl( self, wx.ID_ANY, self.parent.master_address, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer8.Add( self.finish_ip, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer3.Add( bSizer8, 1, wx.EXPAND, 5 )


        bSizer1.Add( bSizer3, 0, wx.EXPAND, 5 )

        bSizer4 = wx.BoxSizer( wx.VERTICAL )

        bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

        self.replace = wx.Button( self, wx.ID_ANY, u"Replace List", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer9.Add( self.replace, 0, wx.ALL, 5 )
        self.Bind(wx.EVT_BUTTON, self.on_replace, self.replace)

        self.add = wx.Button( self, wx.ID_ANY, u"Add to List", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer9.Add( self.add, 0, wx.ALL, 5 )
        self.Bind(wx.EVT_BUTTON, self.on_add, self.add)

        self.save = wx.Button( self, wx.ID_ANY, u"Save as File", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer9.Add( self.save, 0, wx.ALL, 5 )
        self.Bind(wx.EVT_BUTTON, self.on_save, self.save)


        bSizer4.Add( bSizer9, 1, wx.EXPAND, 5 )


        bSizer1.Add( bSizer4, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()
        bSizer1.Fit( self )

        self.Centre( wx.BOTH )

        self.data = []

        self.SetTitle("Generate IP list")


    def on_replace(self, event):
        self.parent.main_list.DeleteAllItems()
        self.on_add(None)

    def on_add(self, event):
        self.gen_list()
        for item in self.data:
            self.parent.main_list.AddObject(self.parent.makeUnit(('','',str(item))))
        self.parent.dumpPickle()
        self.Destroy()

    def on_save(self, event):
        self.gen_list()
        saveFileDialog = wx.FileDialog(
               self, message="Save IP list",
               defaultDir=self.parent.path,
               defaultFile= "generatediplist.csv",
               wildcard="CSV files (*.csv)|*.csv",
               style=wx.SAVE
               )
        if saveFileDialog.ShowModal() == wx.ID_OK:

            path = saveFileDialog.GetPath()
            with open(path, 'wb') as f:
                w = csv.writer(f)
                for item in self.data:
                    w.writerow([item])
                self.Destroy()
        else:
           #dialog.Destroy()
           self.Destroy()
           #return

    def gen_list(self):
        self.data = []
        count = 0
        #try: Later
        start = str(self.start_ip.GetValue())
        start = start.split('.')[3]
        finish = str(self.finish_ip.GetValue())
        finish = finish.split('.')[3]
        for x in range(int(start) , (int(finish)+1)):


            ip = (self.start_ip.GetValue().split('.')[0] + "." +
                   self.start_ip.GetValue().split('.')[1] + "." +
                   self.start_ip.GetValue().split('.')[2] + "." +
                   str(int(start)  + count))
            self.data.append(ip)


            count += 1







