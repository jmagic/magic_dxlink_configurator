"""Menus for Magic DXLink Configurator"""

import wx
import csv
from scripts import mdc_gui

class PreferencesConfig(mdc_gui.Preferences):
    def __init__(self, parent):
        mdc_gui.Preferences.__init__(self, parent)

        self.parent = parent
        self.set_values()

    def set_values(self):
        """Set the field values"""
        self.master_address_txt.SetValue(self.parent.master_address)
        self.device_number_txt.SetValue(self.parent.device_number)
        
        self.success_chk.SetValue(int(self.parent.displaysuccess))
        self.sounds_chk.SetValue(int(self.parent.play_sounds))  
        
        self.time_chk.SetValue(int(self.parent.columns_config[0]))
        self.model_chk.SetValue(int(self.parent.columns_config[1]))
        self.mac_chk.SetValue(int(self.parent.columns_config[2]))
        self.ip_chk.SetValue(int(self.parent.columns_config[3]))
        self.hostname_chk.SetValue(int(self.parent.columns_config[4]))
        self.serial_chk.SetValue(int(self.parent.columns_config[5]))
        self.firmware_chk.SetValue(int(self.parent.columns_config[6]))
        self.device_chk.SetValue(int(self.parent.columns_config[7]))
        self.static_chk.SetValue(int(self.parent.columns_config[8]))
        self.master_chk.SetValue(int(self.parent.columns_config[9]))
        self.system_chk.SetValue(int(self.parent.columns_config[10]))


    def on_ok(self, _):
        """When user clicks ok"""
        self.parent.columns_config = (
            str(int(self.time_chk.GetValue())) +
            str(int(self.model_chk.GetValue())) +
            str(int(self.mac_chk.GetValue())) +
            str(int(self.ip_chk.GetValue())) +
            str(int(self.hostname_chk.GetValue())) +
            str(int(self.serial_chk.GetValue())) +
            str(int(self.firmware_chk.GetValue())) +
            str(int(self.device_chk.GetValue())) +
            str(int(self.static_chk.GetValue())) +
            str(int(self.master_chk.GetValue())) +
            str(int(self.system_chk.GetValue())))

        self.parent.master_address = self.master_address_txt.GetValue()
        self.parent.device_number = self.device_number_txt.GetValue()
        self.parent.displaysuccess = self.success_chk.GetValue()
        self.parent.play_sounds = self.sounds_chk.GetValue()
        self.parent.update_status_bar()
        self.parent.write_config_file()
        self.parent.select_columns()
        self.parent.resize_frame()
        self.Destroy()

    def on_cancel(self, _):
        """When user clicks cancel"""
        self.Destroy()


class DeviceConfig(mdc_gui.DeviceConfiguration):
    def __init__(self, parent, obj):
        mdc_gui.DeviceConfiguration.__init__(self, parent)

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

        if self.hostname == '':
            self.hostname = 'hostname'
        if self.ip_address == '':
            self.ip_address = '0.0.0.0'
        if self.subnet == '':
            self.subnet = '255.255.255.0'
        if self.gateway == ' ':
            self.gateway = '0.0.0.0'
        if self.master == '' or self.master == 'not connected':
            self.master = str(self.parent.master_address)
            
        if self.device == '' or obj.device == '0':
            self.device = str(self.parent.device_number)
            
        self.hostname_txt.SetLabel(self.hostname)

        if obj.ip_type == 's':
            self.dhcp_chk.SetValue(False)
            self.static_chk.SetValue(True)
        else:
            self.dhcp_chk.SetValue(True)
            self.static_chk.SetValue(False)

        self.ip_address_txt.SetLabel(self.ip_address)
        self.subnet_txt.SetLabel(self.subnet)
        self.gateway_txt.SetLabel(self.gateway)
        self.master_txt.SetValue(self.master)
        self.device_txt.SetValue(self.device)

        self.on_dhcp(None) #call to update dhcp / static


    def on_dhcp(self, _):
        """Sets DHCP mode on or off and enables the DHCP options"""

        if self.dhcp_chk.GetValue() == True:
            self.ip_address_txt.Enable(False)
            self.subnet_txt.Enable(False)
            self.gateway_txt.Enable(False)

        else:
            self.ip_address_txt.Enable(True)
            self.subnet_txt.Enable(True)
            self.gateway_txt.Enable(True)


    def on_cancel(self, _):
        """Canel and close"""
        selected_items = self.parent.main_list.GetSelectedObjects()
        selected_items.remove(self.obj)
        self.parent.configure_list.remove(self.obj)
        self.parent.main_list.SelectObjects(selected_items, deselectOthers=True)
        self.Destroy()

    def on_abort(self, _):
        """Quits processing the list of selected items"""
        self.parent.abort = True
        self.parent.main_list.DeselectAll()
        self.Destroy()


    def on_set(self, _):
        """Sends the setting to the device"""
        if self.dhcp_chk.GetValue() == True:
            setdhcp = True
        else:
            setdhcp = False

        info = ['set_device_config',
                self.obj,
                self.parent.telnet_timeout_seconds,
                setdhcp, 
                str(self.hostname_txt.GetValue()),
                str(self.ip_org),
                str(self.ip_address_txt.GetValue()),
                str(self.subnet_txt.GetValue()),
                str(self.gateway_txt.GetValue()),
                str(self.master_txt.GetValue()),
                str(self.device_txt.GetValue())]

        self.parent.telnet_job_queue.put(info)
        self.Destroy()


class IpListGen(mdc_gui.GenerateIP):
    def __init__(self, parent):
        mdc_gui.GenerateIP.__init__(self, parent)

        self.parent = parent

        self.start_txt.SetLabel(self.parent.master_address)
        self.finish_txt.SetLabel(self.parent.master_address)

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
            self.parent.create_add_unit(ip_ad=str(item))
        self.parent.dump_pickle()
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
        start = str(self.start_txt.GetValue())
        start = start.split('.')[3]
        finish = str(self.finish_txt.GetValue())
        finish = finish.split('.')[3]
        for _ in range(int(start), (int(finish)+1)):
            ip_gen = (self.start_txt.GetValue().split('.')[0] + "." +
                      self.start_txt.GetValue().split('.')[1] + "." +
                      self.start_txt.GetValue().split('.')[2] + "." +
                      str(int(start)  + count))
            self.data.append(ip_gen)
            count += 1

class DGXListGen(wx.Dialog):
    def __init__(self, parent):

        wx.Dialog.__init__(self, parent=parent, id=wx.ID_ANY)

        self.parent = parent

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bsizer1 = wx.BoxSizer(wx.VERTICAL)



        bsizer2 = wx.BoxSizer(wx.HORIZONTAL)

        bsizer5 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_statictext1 = wx.StaticText(self, wx.ID_ANY, u"Starting Card", 
                                           wx.DefaultPosition, 
                                           wx.DefaultSize, 0)
        self.m_statictext1.Wrap(-1)
        bsizer5.Add(self.m_statictext1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)


        bsizer2.Add(bsizer5, 0, wx.EXPAND, 5)

        bsizer6 = wx.BoxSizer(wx.VERTICAL)

        self.start_ip = wx.TextCtrl(self, wx.ID_ANY, u'BCPU1',
                                    wx.DefaultPosition, wx.DefaultSize, 0)
        bsizer6.Add(self.start_ip, 0, wx.ALL|wx.EXPAND, 5)


        bsizer2.Add(bsizer6, 1, wx.EXPAND, 5)


        bsizer1.Add(bsizer2, 0, wx.EXPAND, 5)




        bsizer3 = wx.BoxSizer(wx.HORIZONTAL)

        bsizer7 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_statictext2 = wx.StaticText(self, wx.ID_ANY, u"Finishing Card",
                                           wx.DefaultPosition, 
                                           wx.DefaultSize, 0)
        self.m_statictext2.Wrap(-1)
        bsizer7.Add(self.m_statictext2, 0, wx.ALL, 5)


        bsizer3.Add(bsizer7, 0, wx.ALIGN_CENTER_VERTICAL, 5)

        bsizer8 = wx.BoxSizer(wx.VERTICAL)

        self.finish_ip = wx.TextCtrl(self, wx.ID_ANY, 
                                     u'BCPU16', 
                                     wx.DefaultPosition, wx.DefaultSize, 0)
        bsizer8.Add(self.finish_ip, 1, wx.ALL|wx.EXPAND, 5)


        bsizer3.Add(bsizer8, 1, wx.EXPAND, 5)


        bsizer1.Add(bsizer3, 0, wx.EXPAND, 5)




        bsizer14 = wx.BoxSizer(wx.HORIZONTAL)
        
        bsizer11 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_statictext3 = wx.StaticText(self, wx.ID_ANY, u"COM Port",
                                           wx.DefaultPosition, 
                                           wx.DefaultSize, 0)
        self.m_statictext3.Wrap(-1)
        bsizer11.Add(self.m_statictext3, 0, wx.ALL, 5)
        
        bsizer14.Add(bsizer11, 0, wx.ALIGN_CENTER_VERTICAL, 5)
        #bsizer14.Add(bsizer11, 1, wx.EXPAND, 5)
        
        bsizer12 = wx.BoxSizer(wx.VERTICAL)

        self.com_port = wx.TextCtrl(self, wx.ID_ANY, 
                                     u'COM8', 
                                     wx.DefaultPosition, wx.DefaultSize, 0)
        bsizer12.Add(self.com_port, 1, wx.ALL|wx.EXPAND, 5)


        bsizer14.Add(bsizer12, 1, wx.EXPAND, 5)


        bsizer1.Add(bsizer14, 0, wx.EXPAND, 5)



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

        bsizer4.Add(bsizer9, 1, wx.EXPAND, 5)


        bsizer1.Add(bsizer4, 1, wx.EXPAND, 5)


        self.SetSizer(bsizer1)
        self.Layout()
        bsizer1.Fit(self)

        self.Centre(wx.BOTH)

        self.data = []

        self.SetTitle("Generate DGX Card list")
        dlg = wx.MessageDialog(parent=self, message='This will generate ' +
                                   'a list of the BCPU card names for getting' +
                                   ' MSE values from a DGX. Please enter your' +
                                   ' card in the format \'BCPU1\'',
                                   caption='Build DGX list',
                                   style=wx.OK)
        dlg.ShowModal()




    def on_replace(self, _):
        """Replaces list with generated list"""
        self.parent.main_list.DeleteAllItems()
        self.on_add(None)

    def on_add(self, _):
        """Adds to the bottom of the list"""
        self.gen_list()
        for item in self.data:
            self.parent.main_list.AddObject(self.parent.make_unit(
                                            ('', item, 
                                            self.com_port.GetValue())))
        self.parent.dump_pickle()
        self.Destroy()

    def gen_list(self):
        """Generates the IP list"""
        try:
            self.data = []

            start = str(self.start_ip.GetValue()[4:])

            finish = str(self.finish_ip.GetValue()[4:])

            for bcpu in range(int(start), (int(finish)+1)):
                for port in range(4):
                    dgx_gen = 'BCPU' + str(bcpu) + '_Ch' + str(port + 1)
                    self.data.append(dgx_gen)

        except ValueError as error:
            dlg = wx.MessageDialog(parent=self, message='This command didn\'t' +
                                   ' complete. The error text was ' + 
                                    error[0].split(':')[-1] + ' Most likely ' +
                                    'the board name you entered is invalid',
                                   caption='Build DGX list',
                                   style=wx.OK)
            dlg.ShowModal()
            self.Destroy()

