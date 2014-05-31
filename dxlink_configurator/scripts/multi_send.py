"""Sends commands to multiple devices"""

import wx
import os
from pydispatch import dispatcher
import json
from ObjectListView import ObjectListView, ColumnDefn
import time


class MultiSendCommandConfig (wx.Dialog):
    
    def __init__(self, parent, device_list, dxlink_model):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, 
                            pos=wx.DefaultPosition, size=wx.Size(740, 550), 
                            style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        
        bsizer1 = wx.BoxSizer(wx.VERTICAL)
        
        bsizer121 = wx.BoxSizer(wx.VERTICAL)
        
        self.device_list = ObjectListView(self, wx.ID_ANY, 
                                          size=wx.Size(-1, 200), 
                                          style=wx.LC_REPORT|
                                          wx.SUNKEN_BORDER|
                                          wx.RESIZE_BORDER)
        self.device_list.SetColumns([ColumnDefn("Model", "center", 130,
                                                                      "model"),
                                     ColumnDefn("IP", "center", 100, 
                                                                 "ip_address"),
                                     ColumnDefn("Device", "center", 80,
                                                                     "device")])
        bsizer121.Add(self.device_list, 1, wx.ALL|wx.EXPAND, 5)
        bsizer1.Add(bsizer121, 0, wx.EXPAND, 5)
        
        bsizer11 = wx.BoxSizer(wx.HORIZONTAL)
        
        
        self.send_query = wx.RadioButton(self, wx.ID_ANY, u"Query",
                                         wx.DefaultPosition, 
                                         wx.DefaultSize, 0) 
        #wx.RB_GROUP sets the radio buttons as a group. Makes windows work 
        self.Bind(wx.EVT_RADIOBUTTON, self.on_query, self.send_query)
        bsizer11.Add(self.send_query, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        self.send_command = wx.RadioButton(self, wx.ID_ANY, u"Command", 
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        self.send_command.SetValue(True)
        self.Bind(wx.EVT_RADIOBUTTON, self.on_query, self.send_command)
        bsizer11.Add(self.send_command, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        command_combo_choices = []
        self.command_combo = wx.ComboBox(self, wx.ID_ANY, u"Command", 
                                        wx.DefaultPosition, wx.DefaultSize, 
                                        command_combo_choices, 0)
        bsizer11.Add(self.command_combo, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        self.command_combo.Bind(wx.EVT_COMBOBOX, self.on_command_combo)
        
        action_combo_choices = []
        self.action_combo = wx.ComboBox(self, wx.ID_ANY, u"Action", 
                                        wx.DefaultPosition, wx.DefaultSize, 
                                        action_combo_choices, 0)
        bsizer11.Add(self.action_combo, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        self.action_combo.Bind(wx.EVT_COMBOBOX, self.on_action_combo)
        
        self.get_all = wx.CheckBox(self, wx.ID_ANY, u"Send All Query's", 
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        self.get_all.SetValue(False)
        self.get_all.Bind(wx.EVT_CHECKBOX, self.on_get_all)
        bsizer11.Add(self.get_all, 0, wx.ALL, 5)
        
        
        bsizer1.Add(bsizer11, 0, wx.EXPAND, 5)
        
        
        bsizer13 = wx.BoxSizer(wx.HORIZONTAL)
        bsizer20 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.static_text = wx.StaticText(self, wx.ID_ANY, 
                                        u"send_command <DEVICE>:", 
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        self.static_text.Wrap(-1)
        bsizer20.Add(self.static_text, 0, wx.ALIGN_CENTER_VERTICAL|
                                            wx.TOP|wx.BOTTOM|wx.LEFT, 5)
        
        self.string_port = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, 
                                        wx.DefaultPosition, wx.Size(20, -1), 0)
        
        bsizer20.Add(self.string_port, 0, wx.TOP|wx.BOTTOM, 5)
        
        self.static_text2 = wx.StaticText(self, wx.ID_ANY, u":<SYSTEM>, \" \' ",
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.static_text2.Wrap(-1)
        bsizer20.Add(self.static_text2, 0, wx.ALIGN_CENTER_VERTICAL|
                                                wx.TOP|wx.BOTTOM, 5)
        
        self.stringcommand = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, 
                                        wx.DefaultPosition, wx.Size(280, -1), 0)
        bsizer20.Add(self.stringcommand, 0, wx.TOP|wx.BOTTOM|wx.RIGHT, 5)
        
        self.static_text3 = wx.StaticText(self, label="\' \" ")
        bsizer20.Add(self.static_text3, 1, wx.ALL, 5)
        
        self.send = wx.Button(self, wx.ID_ANY, u"Send", wx.DefaultPosition, 
                                wx.DefaultSize, 0)
        bsizer20.Add(self.send, 0, wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.on_send, self.send)
        
        self.exit = wx.Button(self, wx.ID_ANY, u"Exit", 
                                    wx.DefaultPosition, wx.DefaultSize, 0)
        bsizer20.Add(self.exit, 0, wx.ALIGN_BOTTOM|wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.on_exit, self.exit)
        
        bsizer13.Add(bsizer20, 0, wx.EXPAND, 5)
        bsizer1.Add(bsizer13, 0, wx.EXPAND, 5)
 
        bsizer15 = wx.BoxSizer(wx.HORIZONTAL)
        
        bsizer16 = wx.BoxSizer(wx.VERTICAL)
        
        bsizer16.SetMinSize(wx.Size(260, -1)) 
        self.description = wx.TextCtrl(self, wx.ID_ANY, u"Command", 
                                        wx.DefaultPosition, wx.Size(-1, -1), 
                                        style=wx.TE_MULTILINE|wx.TE_READONLY|
                                            wx.HSCROLL)
        self.description.SetMaxLength(0) 
        bsizer16.Add(self.description, 1, wx.ALL|wx.EXPAND, 5)
        
        bsizer15.Add(bsizer16, 0, wx.EXPAND, 5)
        
        bsizer17 = wx.BoxSizer(wx.VERTICAL)
        
        self.syntax = wx.TextCtrl(self, wx.ID_ANY, u"Description", 
                                    wx.DefaultPosition, wx.DefaultSize, 
                                    style=wx.TE_MULTILINE|wx.TE_READONLY|
                                        wx.HSCROLL)
        self.syntax.SetMaxLength(0) 
        bsizer17.Add(self.syntax, 1, wx.ALL|wx.EXPAND, 5)
        
        
        bsizer15.Add(bsizer17, 1, wx.EXPAND, 5)
        
        
        bsizer1.Add(bsizer15, 1, wx.EXPAND, 5)
        
        
        self.SetSizer(bsizer1)
        self.Layout()
        
        self.Centre(wx.BOTH)


        #------------------------------ Done with wxFormBuilder  
           
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
            self.rx_tx_commands = {'rx':{}, 'tx':{}}
            
        
        self.obj = []
        self.port = None
        self.result_string = ''
        self.send.Disable()       
        self.dxlink_model = dxlink_model
        self.on_query(None)
        self.completionlist = []
        self.errorlist = []
        self.waiting_result = True
        self.waiting_delay = True
        self.action_combo.Enable(False)

        self.device_list.CreateCheckStateColumn()
        self.device_list.SetObjects(device_list)
        for obj in self.device_list.GetObjects():
            self.device_list.ToggleCheck(obj)
        self.device_list.RefreshObjects(self.device_list.GetObjects())


        dispatcher.connect(self.collect_completions,
                           signal="Collect Completions", 
                           sender=dispatcher.Any)
        dispatcher.connect(self.collect_errors, 
                           signal="Collect Errors", 
                           sender=dispatcher.Any)
        dispatcher.connect(self.on_result, 
                           signal="send_command result", 
                           sender=dispatcher.Any)
        self.time_out = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_time_out, self.time_out)


    #----------------------------------------------------------------------
    
    def collect_completions(self, sender):
        """Creates a list of completed connections"""
        self.completionlist.append(sender)

    def collect_errors(self, sender):
        """Creates a list of incomplete connections"""
        self.errorlist.append(sender)

    def display_progress(self):
        """Shows progress of connections"""
        if len(self.device_list.GetCheckedObjects()) == 1:

            dlg = wx.ProgressDialog("Attempting connect to selected device",
                                    'Attempting connection to selected device',
                            maximum=len(self.device_list.GetCheckedObjects()),
                            parent=self.parent,
                            style=wx.PD_APP_MODAL
                             | wx.PD_AUTO_HIDE
                             | wx.PD_SMOOTH)

            while ((len(self.completionlist) + len(self.errorlist)) <
                                    len(self.device_list.GetCheckedObjects())):
                count = (len(self.completionlist) + len(self.errorlist))
                time.sleep(.01)
                dlg.Pulse()
        else:
            dlg = wx.ProgressDialog("Attempting connect to selected devices",
                              'Attempting connection to all selected devices',
                            maximum=len(self.device_list.GetCheckedObjects()),
                            parent=self.parent,
                            style=wx.PD_APP_MODAL
                             | wx.PD_AUTO_HIDE
                             | wx.PD_SMOOTH
                             | wx.PD_ELAPSED_TIME)

            while ((len(self.completionlist) + len(self.errorlist)) <
                    len(self.device_list.GetCheckedObjects())):
                count = (len(self.completionlist) + len(self.errorlist))
                dlg.Update(count, "Attempting connection to %s of %s devices" %
                       ((count + 1), len(self.device_list.GetCheckedObjects())))

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
        
        if len(self.completionlist) == 0:
            dlg = wx.MessageDialog(parent=self,
                                   message='Failed to connect to' + 
                                              '\n=======================' + 
                                              ' \n%s ' % errortext,
                                   caption='Failed connection list',
                                   style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        elif len(self.errorlist) == 0:
            dlg = wx.MessageDialog(parent=self,
                                       message='Successfully connected to: \n' +
                                               '=======================' + 
                                               '\n%s' % completiontext,
                                       caption='Connection list',
                                       style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            dlg = wx.MessageDialog(parent=self, 
                                   message='Failed to connect to: \n========' +
                                   '=============== \n%s \n \n' % (errortext) +
                                   'Successfully connected to: \n============' +
                                   '===========' +
                                   ' \n%s' % (completiontext),
                                   caption='Connection list',
                                   style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()

        self.errorlist = []
        self.completionlist = []


    def on_command_combo(self, _):
        """Updates the command combo box"""
        if not self.send_query.GetValue():
            self.action_combo.Enable(True)
        self.action_combo.SetValue('Actions')
        self.update_action_combo(self.command_combo.GetValue())
        self.send.Enable()

        
    def on_action_combo(self, _):
        """Updates the action combo box"""
        self.update_string()
        
    def on_query(self, _):
        """Switches to query or commands"""        
        old = self.command_combo.GetValue()
        self.command_combo.Clear()
        self.description.Clear()
        self.syntax.Clear()
        if self.send_query.GetValue():
            self.command_combo.SetValue('Query')
        else:
            self.command_combo.SetValue('Commands')
        
        for item in sorted(self.rx_tx_commands[self.dxlink_model]):  
            if self.send_query.GetValue():
                if item[:1] == '?': # only add query
                
                    self.command_combo.Append(item)
            else:
                if item[:1] != '?': # only add commands
                    
                    self.command_combo.Append(item)
        
        if self.send_query.GetValue():
            self.action_combo.Enable(False)
            for item in self.command_combo.GetItems():
                if item[1:] == old:
                    self.command_combo.SetValue(item)
                    self.on_command_combo(None)
                    break
                else:
                    self.string_port.Clear()
                    self.stringcommand.Clear()
        else:
            self.action_combo.Enable(False)
            for item in self.command_combo.GetItems():
                if item == old[1:]:
                    self.command_combo.SetValue(item)
                    self.on_command_combo(None)
                    break
                else:
                    self.string_port.Clear()
                    self.stringcommand.Clear()
    
    def update_action_combo(self, selection):
        """Updates action combo box"""
        #phasesList = {"rx": self.rxList , "tx": self.txList ,
        # "mftx": self.mftxList }
        self.action_combo.Clear()
        for item in self.rx_tx_commands[self.dxlink_model][selection][1]:
            self.action_combo.Append(item)
            self.port = self.rx_tx_commands[self.dxlink_model][selection][0]
            self.description.SetValue(self.rx_tx_commands[self.dxlink_model]
                                                                 [selection][2])
            self.syntax.SetValue(self.rx_tx_commands[self.dxlink_model]
                                                                 [selection][3])
        self.action_combo.SetValue("Actions")
        self.update_string()


    def update_string(self):
        """Updates the command string"""
        
        if self.action_combo.GetValue() == "Actions":
            action = ""
        elif self.action_combo.GetValue() == "":
            action = ''
        else:
            action = "-" + self.action_combo.GetValue()
        output = self.command_combo.GetValue() + action 
        self.string_port.SetValue(str(self.port))
        self.stringcommand.SetValue(output)

    def on_get_all(self, _):
        """Send all querys"""
        if self.get_all.GetValue():
            
            self.send.Enable(True)
            self.action_combo.Enable(False)
            self.command_combo.Enable(False)
            self.send_command.Enable(False)
            self.send_query.SetValue(True)
            self.on_query(None)
        else:
            self.action_combo.Enable(False)
            self.command_combo.Enable(True)
            self.send_command.Enable(True)
            self.send.Enable(False)
        
    def on_send(self, _):
        """Send the command string"""
        if self.check_for_none_selected(): 
            return
        self.result_string = ''
        self.errorlist = []
        self.completionlist = []
        if self.get_all.GetValue():
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
                      str(self.string_port.GetValue()) + 
                      ":" + 
                      str(system) + 
                      ", " + 
                      "\"\'" + 
                      str(self.stringcommand.GetValue()) + 
                      "\'\"")
            self.parent.telnet_job_queue.put(['send_command', obj, 
                                     self.parent.telnet_timeout_seconds, 
                                     output, 
                                     str(self.port)])

        self.display_progress()

    def on_send_all(self):
        """Send all is checked"""
        for obj in self.device_list.GetCheckedObjects():
            if obj.device == " ":
                device = 0
            else:
                device = obj.device
            if obj.system == " ":
                system = 0
            else:
                system = obj.system

            total = len(self.command_combo.GetItems()) + 1
            dlg = wx.ProgressDialog('Sending command to selected ' +
                                    'device with results listed ' +
                                    'below ', 
                                    'Sending command to selected ' +
                                    'device with results listed ' +
                                    'below',
                                    maximum=total,
                                    parent=self.parent,
                                    style=wx.PD_APP_MODAL
                                     | wx.PD_CAN_ABORT
                                     | wx.PD_AUTO_HIDE
                                     | wx.PD_SMOOTH)            
                    
            count = 0
             
            for item in self.command_combo.GetItems():
                count += 1                        
                output = ("send_command " + 
                           str(device) + 
                           ":" + 
                           str(self.rx_tx_commands
                                         [self.dxlink_model][item][0]) + 
                           ":" + 
                           str(system) + 
                           ", " + 
                           "\"\'" + 
                           str(item) + 
                           "\'\"") 
                
                #while self.delay_timer.IsRunning():
                #    pass
                self.parent.telnet_job_queue.put(['send_command', obj, 
                        self.parent.telnet_timeout_seconds, output, 
                        str(self.rx_tx_commands[self.dxlink_model][item][0])])
                
                self.time_out.Start(5000)
                self.waiting_result = True
                while self.waiting_result: 
                    (continue_sending, _) = dlg.Update(count,
                                        ('Sending command ' + str(count) + 
                                        ' of ' + str(total - 1) + ' to device ' 
                                        + str(device) +
                                        '\n' + self.result_string))
                    if not continue_sending:
                        self.time_out.Stop()
                        self.waiting_result = False
                        self.result_string = ''
                if not continue_sending:
                    break # this skips the rest of the commands 

                start = time.time()
                while time.time() - start <= .5:
                    pass

            self.time_out.Stop()
            self.result_string = ''
            dlg.Destroy()
        self.display_progress()

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
        self.waiting_result = False 
        self.result_string = sender      
        #self.result.SetLabel('Result:   ' + sender)

        
    def on_exit(self, _):
        """When user exits"""       
        self.Destroy()

    def on_abort(self, _):
        """When user clicks abort"""        
        self.parent.abort = True
        self.Destroy()

        































































































