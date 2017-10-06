"""Sends commands to multiple devices"""

import wx
import os
from pydispatch import dispatcher
import json
from ObjectListView import ObjectListView, ColumnDefn
import time
from scripts import mdc_gui

class SendCommandConfig(mdc_gui.MultiSend):
    def __init__(self, parent, device_list, dxlink_model):
        mdc_gui.MultiSend.__init__(self, parent)
           
        self.parent = parent
        self.SetTitle("Multiple Send Command") # to %s" %obj.ip)
        try:
            #create json file with: 
            #json.dump(jsonData, outfile, sort_keys = True, indent = 4,
            #ensure_ascii=False)
            with open("send_commands\\rx_tx_commands.txt") as command_file:

                self.rx_tx_commands = json.load(command_file)
        except IOError:
            dlg = wx.MessageDialog(parent=self, message='Cannot find  ' +
                                   'rx_tx_commands.txt \nYou will now only be' + 
                                   ' able to send commands manually. \nTo ' + 
                                   'have the system commands auto load, ' +
                                   're-install the \nprogram or replace: ' +
                                   os.getcwd() + '\\send_commands\\' +
                                   'rx_tx_commands.txt',
                                   caption='Please re-install program.',
                                   style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            self.rx_tx_commands = {'dxrx':{}, 
                                   'dxtx':{}, 
                                   'dxftx':{}, 
                                   'dxfrx':{}}
            
        self.device_list = ObjectListView(self.olv_panel, wx.ID_ANY, 
                                          size=wx.Size(-1, 200), 
                                          style=wx.LC_REPORT|
                                          wx.SUNKEN_BORDER|
                                          wx.RESIZE_BORDER)
        self.device_list.SetColumns(
            [ColumnDefn("Model", "center", 130, "model"),
             ColumnDefn("IP", "center", 100, "ip_address"),
             ColumnDefn("Device", "center", 80, "device"),
             ColumnDefn("Status", "left", 120, "status")])

        self.olv_sizer.Add(self.device_list, 1, wx.ALL|wx.EXPAND, 0)
        self.olv_sizer.Layout()

        self.obj = []
        self.port = None
        self.result_string = ''
        self.send_btn.Disable()       
        self.dxlink_model = dxlink_model
        self.on_query(None)
        self.completionlist = []
        self.errorlist = []
        self.waiting_result = True
        self.waiting_delay = True
        self.action_cmb.Enable(False)

        self.device_list.CreateCheckStateColumn()
        self.device_list.SetObjects(device_list)
        for obj in self.device_list.GetObjects():
            self.device_list.ToggleCheck(obj)
        self.device_list.RefreshObjects(self.device_list.GetObjects())
        dispatcher.connect(self.on_result, 
                           signal="send_command result", 
                           sender=dispatcher.Any)

        dispatcher.connect(self.update_window,
                           signal="Update Window",
                           sender=dispatcher.Any)
        self.time_out = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_time_out, self.time_out)

    def on_command_combo(self, _):
        """Updates the command combo box"""
        if not self.query_chk.GetValue():
            self.action_cmb.Enable(True)
        self.action_cmb.SetValue('Actions')
        self.update_action_combo(self.commands_cmb.GetValue())
        self.send_btn.Enable()

        
    def on_action_combo(self, _):
        """Updates the action combo box"""
        self.update_string()
        
    def on_query(self, _):
        """Switches to query or commands"""        
        old = self.commands_cmb.GetValue()
        self.commands_cmb.Clear()
        self.description_txt.Clear()
        self.syntax_txt.Clear()
        if self.query_chk.GetValue():
            self.commands_cmb.SetValue('Query')
        else:
            self.commands_cmb.SetValue('Commands')
        
        for item in sorted(self.rx_tx_commands[self.dxlink_model]):  
            if self.query_chk.GetValue():
                if item[:1] == '?': # only add query
                
                    self.commands_cmb.Append(item)
            else:
                if item[:1] != '?': # only add commands
                    
                    self.commands_cmb.Append(item)
        
        if self.query_chk.GetValue():
            self.action_cmb.Enable(False)
            for item in self.commands_cmb.GetItems():
                if item[1:] == old:
                    self.commands_cmb.SetValue(item)
                    self.on_command_combo(None)
                    break
                else:
                    self.string_port_txt.Clear()
                    self.string_command_txt.Clear()
        else:
            self.action_cmb.Enable(False)
            for item in self.commands_cmb.GetItems():
                if item == old[1:]:
                    self.commands_cmb.SetValue(item)
                    self.on_command_combo(None)
                    break
                else:
                    self.string_port_txt.Clear()
                    self.string_command_txt.Clear()
    
    def update_action_combo(self, selection):
        """Updates action combo box"""

        self.action_cmb.Clear()
        for item in self.rx_tx_commands[self.dxlink_model][selection][1]:
            self.action_cmb.Append(item)
            self.port = self.rx_tx_commands[self.dxlink_model][selection][0]
            self.description_txt.SetValue(
                self.rx_tx_commands[self.dxlink_model][selection][2])
            self.syntax_txt.SetValue(
                self.rx_tx_commands[self.dxlink_model][selection][3])
        self.action_cmb.SetValue("Actions")
        self.update_string()


    def update_string(self):
        """Updates the command string"""
        
        if self.action_cmb.GetValue() == "Actions":
            action = ""
        elif self.action_cmb.GetValue() == "":
            action = ''
        else:
            action = "-" + self.action_cmb.GetValue()
        output = self.commands_cmb.GetValue() + action 
        self.string_port_txt.SetValue(str(self.port))
        self.string_command_txt.SetValue(output)

    def on_get_all(self, _):
        """Send all querys"""
        if self.get_all_chk.GetValue():
            
            self.send_btn.Enable(True)
            self.action_cmb.Enable(False)
            self.commands_cmb.Enable(False)
            self.command_chk.Enable(False)
            self.query_chk.SetValue(True)
            self.on_query(None)
        else:
            self.action_cmb.Enable(False)
            self.commands_cmb.Enable(True)
            self.command_chk.Enable(True)
            self.send_btn.Enable(False)
        
    def on_send(self, _):
        """Send the command string"""
        if self.check_for_none_selected(): 
            return
        self.result_string = ''
        self.errorlist = []
        self.completionlist = []
        if self.get_all_chk.GetValue():
            self.on_send_all()
            return  
        for obj in self.device_list.GetCheckedObjects():
            if obj.device == " ":
                device = 0
            else:
                device = obj.device
            if obj.system == " ":
                system = 0
            else:
                system = obj.system

            output = ("send_command " + 
                      str(device) + 
                      ":" + 
                      str(self.string_port_txt.GetValue()) + 
                      ":" + 
                      str(system) + 
                      ", " + 
                      "\"\'" + 
                      str(self.string_command_txt.GetValue()) + 
                      "\'\"")
            self.parent.telnet_job_queue.put(
                ['send_command', obj, 
                 self.parent.telnet_timeout_seconds, 
                 output])
            self.parent.set_status((obj, "Queued"))
            self.device_list.RefreshObject(obj)

        #self.display_progress()

    def on_send_all(self):
        """Send all is checked"""
        for obj in self.device_list.GetCheckedObjects():
            command_list = []
            for item in self.commands_cmb.GetItems():
                command_list.append(
                    (str(item), 
                     str(self.rx_tx_commands[self.dxlink_model][item][0]))) 
            self.parent.telnet_job_queue.put(
                ['multiple_send_command', obj, 
                 self.parent.telnet_timeout_seconds, 
                 command_list])
            
        
    def update_window(self, sender):
        """Updates objs as they progress"""
        self.device_list.RefreshObject(sender)

    def check_for_none_selected(self):
        """Checks if nothing is selected"""
        if len(self.device_list.GetCheckedObjects()) == 0:
            dlg = wx.MessageDialog(parent=self, message='Nothing selected...' +
                                   '\nPlease use the check box  on the device' +
                                   ' you want to select',
                                   caption='Nothing Selected',
                                   style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return True

    
    def on_time_out(self, _):
        """Timer has expired"""
        self.waiting_result = False
        self.result_string = "*** Timed out waiting for response ***"

    def on_result(self, sender):
        """Sets the result label""" 
        #self.waiting_result = False
        if  sender[0]:
            self.result_string = sender[1] 
        else:
            print("error ", sender[1])
        
    def on_exit(self, _):
        """When user exits"""       
        self.Destroy()

    def on_abort(self, _):
        """When user clicks abort"""        
        self.parent.abort = True
        self.Destroy()

        































































































