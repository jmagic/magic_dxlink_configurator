import wx
from pydispatch import dispatcher
import json
from ObjectListView import ObjectListView, ColumnDefn
import time


class MultiSendCommandConfig ( wx.Dialog ):
    
    def __init__( self, parent, device_list, dxlink_model ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, 
                            pos = wx.DefaultPosition, size = wx.Size( 740,550 ), 
                            style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer121 = wx.BoxSizer( wx.VERTICAL )
        
        self.deviceOlv = ObjectListView(self, wx.ID_ANY, size = wx.Size( -1,200), 
                                        style=wx.LC_REPORT|
                                               wx.SUNKEN_BORDER|
                                               wx.RESIZE_BORDER )
        self.deviceOlv.SetColumns([ColumnDefn("Model", "center", 130, "model"),
                                        ColumnDefn("IP", "center", 100, "ip"),
                                        ColumnDefn("Device", "center", 80, "device")])
        bSizer121.Add( self.deviceOlv, 1, wx.ALL|wx.EXPAND, 5 )
        bSizer1.Add ( bSizer121, 0, wx.EXPAND, 5)
        
        bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
        
        
        self.send_query = wx.RadioButton(self, wx.ID_ANY, u"Query",
                                             wx.DefaultPosition, wx.DefaultSize, 0 ) #wx.RB_GROUP sets the radio buttons as a group. Makes windows work 
        self.Bind(wx.EVT_RADIOBUTTON, self.onQuery, self.send_query)
        bSizer11.Add( self.send_query, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.send_command = wx.RadioButton(self,  wx.ID_ANY, u"Command", 
                                        wx.DefaultPosition, wx.DefaultSize,0 )
        self.send_command.SetValue( True )
        self.Bind(wx.EVT_RADIOBUTTON, self.onQuery, self.send_command)
        bSizer11.Add( self.send_command, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        command_comboChoices = []
        self.command_combo = wx.ComboBox( self, wx.ID_ANY, u"Command", 
                                        wx.DefaultPosition, wx.DefaultSize, 
                                        command_comboChoices, 0 )
        bSizer11.Add( self.command_combo, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        self.command_combo.Bind(wx.EVT_COMBOBOX, self.onCommandCombo)
        
        action_comboChoices = []
        self.action_combo = wx.ComboBox( self, wx.ID_ANY, u"Action", 
                                        wx.DefaultPosition, wx.DefaultSize, 
                                        action_comboChoices, 0 )
        bSizer11.Add( self.action_combo, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        self.action_combo.Bind(wx.EVT_COMBOBOX, self.onActionCombo)
        
        self.get_all = wx.CheckBox( self, wx.ID_ANY, u"Send All Query's", 
                                        wx.DefaultPosition, wx.DefaultSize, 0 )
        self.get_all.SetValue(False)
        self.get_all.Bind(wx.EVT_CHECKBOX, self.onGetAll)
        bSizer11.Add( self.get_all, 0, wx.ALL, 5 )
        
        
        bSizer1.Add( bSizer11, 0, wx.EXPAND, 5 )
        
        
        bSizer13 = wx.BoxSizer( wx.HORIZONTAL )
        bSizer20 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.static_text = wx.StaticText(self, wx.ID_ANY, 
                                        u"send_command <DEVICE>:", 
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        self.static_text.Wrap( -1 )
        bSizer20.Add( self.static_text, 0,  wx.ALIGN_CENTER_VERTICAL|
                                            wx.TOP|wx.BOTTOM|wx.LEFT, 5)
        
        self.string_port = wx.TextCtrl(  self, wx.ID_ANY, wx.EmptyString, 
                                        wx.DefaultPosition, wx.Size( 20,-1 ), 0 )
        
        bSizer20.Add( self.string_port, 0, wx.TOP|wx.BOTTOM, 5  )
        
        self.static_text2 = wx.StaticText(self, wx.ID_ANY, u":<SYSTEM>, \" \' ",
                                          wx.DefaultPosition, wx.DefaultSize, 0 )
        self.static_text2.Wrap( -1 )
        bSizer20.Add( self.static_text2, 0, wx.ALIGN_CENTER_VERTICAL|
                                                wx.TOP|wx.BOTTOM, 5)
        
        self.stringcommand = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, 
                                        wx.DefaultPosition, wx.Size( 280,-1 ), 0)
        bSizer20.Add( self.stringcommand, 0, wx.TOP|wx.BOTTOM|wx.RIGHT, 5)
        
        self.static_text3 = wx.StaticText(self, label="\' \" ")
        bSizer20.Add( self.static_text3, 1, wx.ALL, 5)
        
        self.send = wx.Button( self, wx.ID_ANY, u"Send", wx.DefaultPosition, 
                                wx.DefaultSize, 0 )
        bSizer20.Add( self.send, 0, wx.ALL, 5 )
        self.Bind(wx.EVT_BUTTON, self.onSend, self.send)
        
        self.exit = wx.Button( self, wx.ID_ANY, u"Exit", 
                                    wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer20.Add( self.exit, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )
        self.Bind(wx.EVT_BUTTON, self.OnExit, self.exit)
        
        bSizer13.Add( bSizer20, 0, wx.EXPAND, 5 )
        bSizer1.Add( bSizer13, 0, wx.EXPAND, 5 )
 
        bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
        
        bSizer16 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer16.SetMinSize( wx.Size( 260,-1 ) ) 
        self.description = wx.TextCtrl( self, wx.ID_ANY, u"Command", 
                                        wx.DefaultPosition, wx.Size( -1,-1 ), 
                                        style=wx.TE_MULTILINE|wx.TE_READONLY|
                                            wx.HSCROLL )
        self.description.SetMaxLength( 0 ) 
        bSizer16.Add( self.description, 1, wx.ALL|wx.EXPAND, 5 )
        
        bSizer15.Add( bSizer16, 0, wx.EXPAND, 5 )
        
        bSizer17 = wx.BoxSizer( wx.VERTICAL )
        
        self.syntax = wx.TextCtrl( self, wx.ID_ANY, u"Description", 
                                    wx.DefaultPosition, wx.DefaultSize, 
                                    style=wx.TE_MULTILINE|wx.TE_READONLY|
                                        wx.HSCROLL )
        self.syntax.SetMaxLength( 0 ) 
        bSizer17.Add( self.syntax, 1, wx.ALL|wx.EXPAND, 5 )
        
        
        bSizer15.Add( bSizer17, 1, wx.EXPAND, 5 )
        
        
        bSizer1.Add( bSizer15, 1, wx.EXPAND, 5 )
        
        
        self.SetSizer( bSizer1 )
        self.Layout()
        
        self.Centre(wx.BOTH)


        #------------------------------ Done with wxFormBuilder  
           
        self.parent = parent
        self.parent.actionItems = []  #cleared out so progress will work.
        self.SetTitle("Multiple Send Command") # to %s" %obj.ip)
        try:
            #create json file with: 
            #json.dump(jsonData, outfile, sort_keys = True, indent = 4,
            #ensure_ascii=False)
            with open("scripts\\rx_tx_commands.txt") as command_file:

                self.rx_tx_commands = json.load(command_file)
        except IOError:
            dlg = wx.MessageDialog(parent=self, message='Cannot find  ' +
                                   'rx_tx_commands.txt \nYou will be able ' +
                                   'to send commands manually, to have the ' +
                                   'system commands auto load re-install the ' +
                                   'program or replace scripts\\' +
                                   'rx_tx_commands.txt',
                                   caption='Please re-install program.',
                                   style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            self.rx_tx_commands = {'rx':{},'tx':{}}
            
        
        self.obj = []
        self.result_string = ''
        self.send.Disable()       
        self.dxlink_model = dxlink_model
        self.onQuery(None)
        self.deviceOlv.SetColumns([ColumnDefn("Model", "center", 130, "model"),
                                   ColumnDefn("IP", "center", 100, "ip"),
                                   ColumnDefn("Device", "center", 80, "device")])
        self.deviceOlv.CreateCheckStateColumn()
        self.deviceOlv.SetObjects(device_list)
        objects = self.deviceOlv.GetObjects()
        for obj in objects:
            self.deviceOlv.ToggleCheck(obj)
        self.deviceOlv.RefreshObjects(objects)
        self.waiting_result = True
        dispatcher.connect(self.result, signal="send_command result", 
                            sender = dispatcher.Any)
        self.time_out = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimeOut, self.time_out) 
    #----------------------------------------------------------------------
    def onCommandCombo(self, event):

        self.action_combo.SetValue('Actions')
        self.updateActionCombo(self.command_combo.GetValue())
        self.send.Enable()
        
    def onActionCombo(self, event):
       
        self.updateString()
        pass
        
    def onQuery(self, event):
        
        old = self.command_combo.GetValue()
        self.command_combo.Clear()
        self.description.Clear()
        self.syntax.Clear()
        if self.send_query.GetValue():
            self.command_combo.SetValue('Query')
        else:
            self.command_combo.SetValue('Commands')
        
        for item in sorted(self.rx_tx_commands[self.dxlink_model]):  #sorting by second dimension 
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
                    self.onCommandCombo(None)
                    break
                else:
                    self.string_port.Clear()
                    self.stringcommand.Clear()
        else:
            self.action_combo.Enable(True)
            for item in self.command_combo.GetItems():
                if item == old[1:]:
                    self.command_combo.SetValue(item)
                    self.onCommandCombo(None)
                    break
                else:
                    self.string_port.Clear()
                    self.stringcommand.Clear()
    
    def updateActionCombo(self, selection):
        #phasesList = {"rx": self.rxList , "tx": self.txList , "mftx": self.mftxList }
        self.action_combo.Clear()
        for item in self.rx_tx_commands[self.dxlink_model][selection][1]:
            #print item
            self.action_combo.Append(item)
            self.port = self.rx_tx_commands[self.dxlink_model][selection][0]
            self.description.SetValue(self.rx_tx_commands[self.dxlink_model][selection][2])
            self.syntax.SetValue(self.rx_tx_commands[self.dxlink_model][selection][3])
        self.action_combo.SetValue("Actions")
        self.updateString()


    def updateString(self, Data=None):
        
        if self.action_combo.GetValue() == "Actions":
            action = ""
        elif self.action_combo.GetValue() == "":
                action = ''
        else:
            action = "-" + self.action_combo.GetValue()
        output = self.command_combo.GetValue() + action 
        self.string_port.SetValue(str(self.port))
        self.stringcommand.SetValue(output)

    def onGetAll(self, event):
        if self.get_all.GetValue():
            
            self.send.Enable(True)
            self.action_combo.Enable(False)
            self.command_combo.Enable(False)
            self.send_command.Enable(False)
            self.send_query.SetValue(True)
            self.onQuery(None)
        else:
            self.action_combo.Enable(True)
            self.command_combo.Enable(True)
            self.send_command.Enable(True)
            self.send.Enable(False)
        
    def onResult(self, sender):
        
        self.results.SetLabel('Result:   ' + sender)

    def onSend(self, event):
        
        objects = self.deviceOlv.GetObjects()
        for obj in objects:
            if self.deviceOlv.IsChecked(obj):
                #self.updateString(obj)
                if obj.device == " ":
                    device = 0
                else:
                    device = obj.device
                if obj.system == " ":
                    system = 0
                else:
                    system = obj.system
                
                if self.get_all.GetValue():
                    total = len(self.command_combo.GetItems())
                    #print total
                    dlg = wx.ProgressDialog("Sending command to selected device with results listed below ",'Sending command to selected device',
                            maximum = total,
                            parent = self.parent,
                            style =  wx.PD_APP_MODAL
                             | wx.PD_CAN_ABORT
                             | wx.PD_AUTO_HIDE
                             | wx.PD_SMOOTH
                             #| wx.PD_ELAPSED_TIME 
                             )
            
                            
                    count = 0 
                    abort = False
                    for item in self.command_combo.GetItems():
                        count += 1
                        #print count
                        #self.command_combo.SetValue(item)
                        #print item
                        #self.onCommandCombo(None)
                        
                        #print self.command_combo.GetValue()
                        
                        output = "send_command " + str(device) + ":" + str(self.rx_tx_commands[self.dxlink_model][item][0]) + ":" + str(system) + ", " + "\"\'" + str(item) + "\'\""
                        #print output
                        info = ['SendCommand', obj, self.parent.telnet_timeout_seconds, output, str(self.rx_tx_commands[self.dxlink_model][item][0])]
                        #print info
                        self.parent.actionItems.append(obj)
                        self.parent.telnetjobqueue.put(['SendCommand', obj, self.parent.telnet_timeout_seconds, output , str(self.rx_tx_commands[self.dxlink_model][item][0])])
                        #time_out = 0
                        self.time_out.Start(5000)
                        while self.waiting_result:
                            
                                   
                             
                            time.sleep(.5)
                            #time_out += 1
                            #if time_out >= 5:
                            #    self.waiting_result = False
                            (abort, skip) = dlg.Update (count,("Sending command %s of %s to device %s \n" + self.result_string) % (count,total,device))
                            #print abort
                        if not abort:
                            #self.parent.displayProgress()
                            abort = False
                            self.time_out.Stop()
                            self.waiting_result = True
                            break
                        self.time_out.Stop()
                        self.waiting_result = True
                        
                    #self.parent.actionItems = []
                    #self.completionlist = []
                    #self.errorlist = []
                    self.parent.displayProgress()
                    self.result_string = ''
                    dlg.Destroy()
                        
                        
                
                else:
                    output = "send_command " + str(device) + ":" + str(self.string_port.GetValue()) + ":" + str(system) + ", " + "\"\'" + str(self.stringcommand.GetValue()) + "\'\""
                    #print output
                    info = ['SendCommand', obj, self.parent.telnet_timeout_seconds, output , str(self.port)]
                    self.parent.actionItems.append(obj)
                    self.parent.telnetjobqueue.put(['SendCommand', obj, self.parent.telnet_timeout_seconds, output , str(self.port)])
                
                    self.parent.displayProgress()
    
    def onTimeOut(self, event):
        self.waiting_result = False
        #print 'timeout'
    
    def result(self, sender):
    
        self.waiting_result = False
        self.result_string = sender
        #print sender
        #time.sleep(1)
        #print result maybe
        
    def OnExit(self, event):

        self.Destroy()
        
    def OnAbort(self, event):
        
        self.parent.abort = True
        self.Destroy()
            
    def getModelandDevice(self):
        
        if self.obj.model == ' ' or self.obj.model == '' or self.obj.device == ' ' or self.obj.device == '':
            self.parent.jobqueue.put(['GetTelnetInfo', self.obj,  self.parent.telnet_timeout_seconds])
            self.parent.actionItems.append(self.obj)
            self.parent.displayProgress()         
        if self.obj.model[12:14] == 'TX' or self.obj.model[12:14] == 'WP'or self.obj.model[12:15] == 'DWP'or self.obj.model[12:16] == 'MFTX':
            self.dxlink_model = 'tx'
        elif self.obj.model[12:14] == 'RX':
            self.dxlink_model = 'rx'
        else:
            self.NotDXLink()  

    def NotDXLink(self):
        
        dlg = wx.MessageDialog(parent=self, message= 'This does not appear to be a DXLink Device \n Do you want to continue?', 
                                   caption = 'Do you want to continue?',
                                   style = wx.OK | wx.CANCEL
                                   )
        if  dlg.ShowModal() == wx.CANCEL:
            self.parent.abort = True
            dlg.Destroy()
            self.Destroy()
        else:
            dlg.Destroy()
            self.dxlink_model = 'tx'
            self.obj.device = '0'
        '''self.lblname = wx.StaticText(self, label="This is not a DXLink Device", pos=(20,40))

        self.cancel = wx.Button(self, label="Cancel", pos=(225, 40))
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancel)
        
        self.SetSize((220,220))'''
    
     
        































































































