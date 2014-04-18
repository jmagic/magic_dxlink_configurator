"""Configurator is a program that integrates unit discovery and telnet commands 
to ease configuration and management of AMX DXLink devices.

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

from scripts import (config_menus, dhcp_sniffer, multi_send, multi_ping, \
                    plot_class, telnet_class, telnetto_class)

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
        self.mac = mac
        self.ip = ip_ad
        self.arrival_time = arrival_time
        self.ip_type = ip_type
        self.gateway = gateway
        self.subnet = subnet
        self.master = master
        self.system = system


class MainPanel(wx.Panel):

    #----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY)

        self.parent = parent
        self.readConfigFile()
        self.resizeFrame()
        self.name = "Magic DXLink Configurator"
        self.version = "v1.5.3"

        self.setTitleBar()

        # Set up some variables
        #self.AMX_only_filter = False #disable the AMX filter by default
        self.errorlist = []
        self.completionlist = []
        self.mse_active_list = []
        self.port_error = False
        self.ping_objects = []
        self.ping_active = False

        # Build the ObjectListView
        self.main_list = ObjectListView(self, wx.ID_ANY, 
                                      style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.main_list.cellEditMode = ObjectListView.CELLEDIT_DOUBLECLICK
        self.main_list.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, parent.onRightClick)
        self.main_list.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)

        # Select columns displayed
        self.columns = []

        self.columns_setup = [  ColumnDefn("Time", "center", 90, "arrival_time",
                                           stringConverter="%I:%M:%S%p"),
                                ColumnDefn("Model", "center", 130, "model"),
                                ColumnDefn("MAC", "center", 130, "mac"),
                                ColumnDefn("IP", "center", 100, "ip"),
                                ColumnDefn("Hostname", "left", 130, "hostname"),
                                ColumnDefn("Serial Number","center", 150, "serial"),
                                ColumnDefn("Firmware", "center", 80, "firmware"),
                                ColumnDefn("Device", "center", 80, "device"),
                                ColumnDefn("Static", "center", 60, "ip_type"),
                                ColumnDefn("Master", "center", 100, "master"),
                                ColumnDefn("System", "center", 80, "system")
                             ]

        self.selectColumns()
        #reload last known data set
        self.loadDataPickle()
        self.update_status_bar()

        # Create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.main_list, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(mainSizer)

        # Create DHCP listening thread
        self.SniffDHCPThread = dhcp_sniffer.SniffDHCPThread(self)
        self.SniffDHCPThread.setDaemon(True)
        self.SniffDHCPThread.start()

        # create a telenetto thread pool and assign them to a queue
        self.telnettoqueue = Queue.Queue()
        for i in range(10):
            self.TelnettoThread = telnetto_class.TelnetToThread(self, self.telnettoqueue)
            self.TelnettoThread.setDaemon(True)
            self.TelnettoThread.start()


        # create a telnetjob thread pool and assign them to a queue
        self.telnetjobqueue = Queue.Queue()
        for i in range(int(self.thread_number)):
            self.TelnetJobThread = telnet_class.Telnetjobs(self, self.telnetjobqueue)
            self.TelnetJobThread.setDaemon(True)
            self.TelnetJobThread.start()

        # Setup our dispatcher listeners for the threads
        dispatcher.connect(self.updateInfo, signal="Incoming Packet", sender = dispatcher.Any)
        dispatcher.connect(self.collectCompletions, signal="Collect Completions", sender = dispatcher.Any)
        dispatcher.connect(self.collectErrors, signal="Collect Errors", sender = dispatcher.Any)
    #----------------------------------------------------------------------

    def onKeyDown(self,event):
        key = event.GetKeyCode()
        if key == wx.WXK_DELETE:
            dlg = wx.MessageDialog(parent=self,
                  message=
            'Are you sure? \n\nThis will delete all selected items in the list',
                                   caption = 'Delete All Selected Items',
                                   style = wx.OK|wx.CANCEL
                                   )

            if dlg.ShowModal() == wx.ID_OK:
                self.deleteItem()
                self.dumpPickle()
            else:
                return
        event.Skip()

    def playSound(self):
        if self.play_sounds:
            try:
                winsound.PlaySound("woof.wav", winsound.SND_FILENAME)
            except:
                pass

    def collectCompletions(self, sender):
        self.completionlist.append(sender)

    def collectErrors(self, sender):
        self.errorlist.append(sender)

    def portErrors(self):
        dlg = wx.MessageDialog(self.parent,
                               message= 'Unable to use port 67\n No DHCP requests will be added.',
                               caption = 'Port in use',
                               style = wx.ICON_INFORMATION
                               )
        dlg.ShowModal()
        self.parent.listenfilter.Enable(False)
        self.parent.listenDHCP.Enable(False)


    def displayProgress(self, data=None):
        if len(self.main_list.GetSelectedObjects()) == 1:

            dlg = wx.ProgressDialog("Attempting connect to selected device",
                                    'Attempting connection to selected device',
                                    maximum = len(self.main_list.GetSelectedObjects()),
                                    parent = self.parent,
                                    style =  wx.PD_APP_MODAL
                                     | wx.PD_AUTO_HIDE
                                     | wx.PD_SMOOTH
                                     #| wx.PD_ELAPSED_TIME
                                     )

            while ((len(self.completionlist) + len(self.errorlist)) <
                                    len(self.main_list.GetSelectedObjects())):
                count = (len(self.completionlist) + len(self.errorlist))
                time.sleep(.01)
                dlg.Pulse()
        else:
            dlg = wx.ProgressDialog("Attempting connect to selected devices",
                                  'Attempting connection to all selected devices',
                                maximum = len(self.main_list.GetSelectedObjects()),
                                parent = self.parent,
                                style =  wx.PD_APP_MODAL
                                 | wx.PD_AUTO_HIDE
                                 | wx.PD_SMOOTH
                                 | wx.PD_ELAPSED_TIME
                                 )

            while ((len(self.completionlist) + len(self.errorlist)) <
                                        len(self.main_list.GetSelectedObjects())):
                count = (len(self.completionlist) + len(self.errorlist))
                dlg.Update (count,"Attempting connection to %s of %s devices" %
                            ((count + 1),len(self.main_list.GetSelectedObjects())))

        dlg.Destroy()
        self.main_list.RefreshObjects(self.main_list.GetSelectedObjects())
        self.dumpPickle()

        errortext = ""
        phil =" "
        #print self.errorlist
        for i in xrange(len(self.errorlist)):
            while (len(self.errorlist[i][0]) + (len(phil) - 1)) < 15:
                phil = phil + " "
            errortext = errortext + self.errorlist[i][0] + " " + phil + " " +  \
                        self.errorlist[i][1] + "\n"
            phil = " "

        completiontext = ""
        for i in xrange(len(self.completionlist)):
            completiontext = completiontext + self.completionlist[i][0] + "\n"
        #print errortext
        if (len(self.errorlist) == len(self.main_list.GetSelectedObjects())):
            dlg = wx.MessageDialog(parent=self,
                                   message= ('Failed to connect to' + \
                                              'n=======================' + \
                                              ' \n%s ') % errortext ,
                                   caption = 'Failed connection list',
                                   style = wx.OK
                                   )
            dlg.ShowModal()
            dlg.Destroy()

        elif (len(self.completionlist) == len(self.main_list.GetSelectedObjects())):
            if self.displaysuccess:
                dlg = wx.MessageDialog(parent=self,
                                       message= 'Successfully connected to: \n======================= \n%s' % completiontext ,
                                       caption = 'Connection list',
                                       style = wx.OK
                                       )
                dlg.ShowModal()
                dlg.Destroy()

        else:
            dlg = wx.MessageDialog(parent=self, message= 'Failed to connect to: \n======================= \n%s \n \nSuccessfully connected to: \n======================= \n%s' % (errortext,completiontext) ,
                                   caption = 'Connection list',
                                   style = wx.OK
                                   )
            dlg.ShowModal()
            dlg.Destroy()

        #self.main_list.RefreshObjects(self.actionItems)
        self.dumpPickle()
        self.errorlist = []
        self.completionlist = []
        self.singleSelect = []


    def toggleDHCPsniffing(self, event):

        self.dhcp_sniffing = not self.dhcp_sniffing
        self.writeConfigFile()


    def togglefilterAMX(self, data=None):

        self.AMX_only_filter = not self.AMX_only_filter
        self.writeConfigFile()

    def selectColumns(self):

        self.columns = []
        for i in range(len(self.columns_setup)):
            self.columns.append((int(self.columns_config[i]),self.columns_setup[i]))

        todisplay = []
        for item in self.columns:
            if item[0] == 1:

                todisplay.append(item[1])

        self.main_list.SetColumns(todisplay)

    def getRowInfo(self):
        self.actionItems = self.main_list.GetSelectedObjects()

        if self.actionItems == []:


            dlg = wx.MessageDialog(parent=self, message= 'Nothing selected.... \nPlease click on the device you want to select',
                                   caption = 'Nothing Selected',
                                   style = wx.OK
                                   )
            dlg.ShowModal()
            dlg.Destroy()

    def onSelectAll(self, data=None):
        self.main_list.SelectAll()


    def onSelectNone(self, data=None):
        self.main_list.DeselectAll()


    def telnetTo( self, data=None ):
        if len(self.main_list.GetSelectedObjects()) == 0:return
        if len(self.main_list.GetSelectedObjects()) > 10:
            dlg = wx.MessageDialog(parent=self, message= 'I can only telnet to 10 devices at a time \nPlease select less than ten devices at once',
                                   caption = 'How many telnets?',
                                   style = wx.OK
                                   )
            dlg.ShowModal()
            dlg.Destroy()
            return
        if self.os_type == 'nt':
            if os.path.exists((self.path + self.telnet_client)):

                for obj in self.main_list.GetSelectedObjects():
                    self.telnettoqueue.put(obj)
            else:
                dlg = wx.MessageDialog(parent=self, message= 'Could not find telnet client \nPlease put %s in \n%s' % (self.telnet_client, self.path),
                                       caption = 'No %s' % self.telnet_client,
                                       style = wx.OK
                                       )
                dlg.ShowModal()
                dlg.Destroy()
            return

        if self.os_type == 'posix':
            for obj in self.main_list.GetSelectedObjects():
                self.telnettoqueue.put(obj)

    def plotMSE(self, data=None):
        if len(self.main_list.GetSelectedObjects()) == 0:return
        if len(self.main_list.GetSelectedObjects()) > 10:
            dlg = wx.MessageDialog(parent=self, message= 'I can only graph 10 devices at a time \nPlease select less than ten devices at once',
                                   caption = 'How many graphs?',
                                   style = wx.OK
                                   )
            dlg.ShowModal()
            dlg.Destroy()
            return

        for obj in self.main_list.GetSelectedObjects():
            if (obj.mac in self.mse_active_list):
                dlg = wx.MessageDialog(parent=self, message= 'You are already graphing this MAC address',
                                       caption = 'Are you crazy?',
                                       style = wx.OK
                                       )
                dlg.ShowModal()
                dlg.Destroy()
                return
            self.mse_active_list.append(obj.mac)
            self.telnetjobqueue.put(['MSE', obj, self.telnet_timeout_seconds])
            dia = plot_class.Multi_Plot(self, obj, '-1500')
            dia.Show()

    def multiPing(self, data=None):
        
        self.getRowInfo()
        if len(self.actionItems) == 0:return
        if self.ping_active:
            dlg = wx.MessageDialog(parent=self, message= 'You already have a ping window open', 
                                       caption = 'Are you crazy?',
                                       style = wx.OK
                                       )
            dlg.ShowModal()
            dlg.Destroy()
            return    
            
        self.ping_active = True
        #for obj in self.actionItems:
            
        #self.telnetjobqueue.put(['MSE', obj, self.telnet_timeout_seconds])
        dia = multi_ping.MultiPing(self, self.actionItems)
        dia.Show()

    def factoryAV(self, event):
        if len(self.main_list.GetSelectedObjects()) == 0: return

        for obj in self.main_list.GetSelectedObjects():
            self.telnetjobqueue.put(['FactoryAV', obj, self.telnet_timeout_seconds, 'FACTORYAV', 1])
        self.displayProgress()


    def resetFactory(self, event):
        if len(self.main_list.GetSelectedObjects()) == 0: return
        for obj in self.main_list.GetSelectedObjects():
            dlg = wx.MessageDialog(parent=self, message= 'Are you sure? \n This will reset %s' % obj.ip,
                                   caption = 'Factory Reset',
                                   style = wx.OK|wx.CANCEL
                                   )
            if dlg.ShowModal() == wx.ID_OK:
                dlg.Destroy()
                self.telnetjobqueue.put(['SetFactory', obj, self.telnet_timeout_seconds])
            else:
                return
        self.displayProgress()


    def rebootUnit(self, event):
        if len(self.main_list.GetSelectedObjects()) == 0: return
        for obj in self.main_list.GetSelectedObjects():
            self.telnetjobqueue.put(['SetReboot', obj, self.telnet_timeout_seconds])
        self.displayProgress()


    def openURL(self, event):
        if len(self.main_list.GetSelectedObjects()) == 0: return
        for obj in self.main_list.GetSelectedObjects():
            url = 'http://' + obj.ip
            # Open URL in a new tab, if a browser window is already open.
            webbrowser.open_new_tab(url)


    def getTelnetInfo( self, event):
        if len(self.main_list.GetSelectedObjects()) == 0: return
        for obj in self.main_list.GetSelectedObjects():
            self.telnetjobqueue.put(['GetTelnetInfo', obj,  self.telnet_timeout_seconds])
        self.displayProgress()

    def turnOnLED(self, event):
        if len(self.main_list.GetSelectedObjects()) == 0: return
        for obj in self.main_list.GetSelectedObjects():
            self.telnetjobqueue.put(['TurnOnLED', obj,  self.telnet_timeout_seconds])
        self.displayProgress()

    def turnOffLED(self, event):
        if len(self.main_list.GetSelectedObjects()) == 0: return
        for obj in self.main_list.GetSelectedObjects():
            self.telnetjobqueue.put(['TurnOffLED', obj,  self.telnet_timeout_seconds])
        self.displayProgress()

    def sendCommands(self, event):
        if len(self.main_list.GetSelectedObjects()) == 0: return
        self.tx_devices = []
        self.rx_devices = []
        for obj in self.main_list.GetSelectedObjects():
            if obj.model[12:14] == 'TX' or obj.model[12:14] == 'WP'or obj.model[12:15] == 'DWP'or obj.model[12:16] == 'MFTX':
                self.tx_devices.append(obj)
            elif obj.model[12:14] == 'RX':
                self.rx_devices.append(obj)
            else:
                pass
        if len(self.tx_devices) != 0:
            dia = multi_send.MultiSendCommandConfig(self, self.tx_devices, 'tx')
            dia.ShowModal()
            dia.Destroy()
        if len(self.rx_devices) != 0:
            dia = multi_send.MultiSendCommandConfig(self, self.rx_devices, 'rx')
            dia.ShowModal()
            dia.Destroy()
        if (len(self.tx_devices)+len(self.rx_devices)) == 0:
            dlg = wx.MessageDialog(parent=self, message= 'No DXLink Devices Selected',
                                   caption = 'Cannot send commands',
                                   style = wx.OK
                                   )
            dlg.ShowModal()
            dlg.Destroy()

    def dumpPickle(self):
        pickle.dump(self.main_list.GetObjects(), open((self.path + 'data_store.pkl') , 'wb'))

    def removeAndStore( self, event):
        if len(self.main_list.GetSelectedObjects()) == 0:
            return
        saveFileDialog = wx.FileDialog(
                       self, message="Select file to add units to or create a new file",
                       defaultDir=self.path,
                       defaultFile= "",
                       wildcard="CSV files (*.csv)|*.csv",
                       style=wx.SAVE
                       )
        if saveFileDialog.ShowModal() == wx.ID_OK:
            path = saveFileDialog.GetPath()
            dlg = wx.ProgressDialog("Storing Device Information","Storing Device Information",
                                    maximum = len(self.main_list.GetSelectedObjects()),
                                    parent = self,
                                    style =  wx.PD_APP_MODAL
                                     | wx.PD_AUTO_HIDE
                                     | wx.PD_ELAPSED_TIME
                                     )
            count = 0
            with open(path, 'a') as f:
                for obj in self.main_list.GetSelectedObjects():
                    count += 1
                    dlg.Update(count)
                    data = [obj.model,
                            obj.hostname,
                            obj.serial,
                            obj.firmware,
                            obj.device,
                            obj.mac,
                            obj.ip,
                            obj.arrival_time,
                            obj.ip_type,
                            obj.gateway,
                            obj.subnet,
                            obj.master,
                            obj.system
                            ]
                    w = csv.writer(f, quoting=csv.QUOTE_ALL)
                    w.writerow(data)
            self.main_list.RemoveObjects(self.main_list.GetSelectedObjects())
            self.main_list.RepopulateList()
            self.dumpPickle()

    def importCSVfile( self, event):
        openFileDialog = wx.FileDialog(
                       self, message="Import a CSV file",
                       defaultDir=self.path,
                       defaultFile= "",
                       wildcard="CSV files (*.csv)|*.csv",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_OK:
            openFileDialog.Destroy()
            self.main_list.DeleteAllItems()
            with open( openFileDialog.GetPath() ,'rb') as csvfile:
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
                                 datetime.datetime.strptime((item[7]),"%Y-%m-%d %H:%M:%S.%f"), #will not wrap
                                 item[8],
                                 item[9],
                                 item[10],
                                 item[11],
                                 item[12]
                                )
                    self.main_list.AddObject(data)
            self.dumpPickle()
        else:
            openFileDialog.Destroy()

    def importPlot(self, event):
        openFileDialog = wx.FileDialog(
                       self, message="Import a plot CSV file",
                       defaultDir=self.path,
                       defaultFile= "",
                       wildcard="CSV files (*.csv)|*.csv",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_OK:
            openFileDialog.Destroy()
            with open( openFileDialog.GetPath() ,'rb') as csvfile:
                csv_data = csv.reader(csvfile)
                header = csv_data.next()
                plotObject = []
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
                         ''
                        )
                plotObject.append(data)
                obj =  plotObject[0]
                row_count = (sum(1 for row in csv_data)-1)*-1
                dia = plot_class.Multi_Plot(self, obj, row_count)
                dia.Show()
            with open( openFileDialog.GetPath() ,'rb') as csvfile:  # opening it again to start at top
                csv_data = csv.reader(csvfile)
                header = csv_data.next()
                plotObject = []
                data = [Unit(
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
                         ''
                        )
                    ]
                plotObject.append(data[0])
                obj =  plotObject[0]
                self.mse_active_list.append(obj.mac)
                for item in csv_data:
                    mse = []
                    data = []
                    for i in range(4):
                        data.append(item[i+1])
                        #print data
                    mse_time = [datetime.datetime.strptime((item[0]),'%H:%M:%S.%f'),data]
                    mse.append(mse_time)
                    mse.append(header[5])
                    mse.append(header[6])
                    #print mse
                    #time.sleep(.1)
                    dispatcher.send(signal="Incoming MSE", sender=mse)
        else:
            openFileDialog.Destroy()

    def importIPlist(self, event):
        openFileDialog = wx.FileDialog(
                                       self, message="Open IP List",
                                       defaultDir=self.path,
                                       defaultFile= "",
                                       wildcard="CSV files (*.csv)|*.csv",
                                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
                                       )

        if openFileDialog.ShowModal() == wx.ID_OK:
            self.main_list.DeleteAllItems()
            with open(openFileDialog.GetPath(),'rb') as csvfile:
                cvs_data = csv.reader(csvfile)
                for item in cvs_data:
                    data = Unit(
                                 ' ',
                                 ' ',
                                 ' ',
                                 ' ',
                                 ' ',
                                 ' ',
                                 item[0],
                                 datetime.datetime.now(),
                                 ' ',
                                 ' ',
                                 ' ',
                                 ' ',
                                 ' '
                                )
                    self.main_list.AddObject(data)
            self.dumpPickle()
            openFileDialog.Destroy()
        else:
            openFileDialog.Destroy()

    def generateList(self, event):
        dia = config_menus.IpListGen(self)
        dia.ShowModal()
        dia.Destroy()

    def addLine(self, data=None):
        data =  Unit(
                         ' ',
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
        self.dumpPickle()

    def deleteItem(self, data=None):
        if len(self.main_list.GetSelectedObjects()) == len(self.main_list.GetObjects()):
            self.main_list.DeleteAllItems()
            self.dumpPickle()
            return
        if len(self.main_list.GetSelectedObjects()) == 0:
            return
        self.main_list.RemoveObjects(self.main_list.GetSelectedObjects())
        self.dumpPickle()

    def deleteAllItems(self, data=None):
        dlg = wx.MessageDialog(parent=self, message= 'Are you sure? \n This will delete all items in the list',
                                   caption = 'Delete All Items',
                                   style = wx.OK|wx.CANCEL
                                   )
        if dlg.ShowModal() == wx.ID_OK:
            self.main_list.DeleteAllItems()
            self.dumpPickle()
        else:
            return

    def makeUnit(self, sender):
        # (hostname,mac,ip)
        data = Unit(    '',
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
                        ''
                    )
        return(data)

    def updateInfo(self, sender):
        """
        Receives dhcp requests with and adds them to objects to display
        """
        data = self.makeUnit(sender)
        self.parent.status_bar.SetStatusText('%s -- %s %s %s' %(data.arrival_time.strftime('%I:%M:%S%p'), data.hostname, data.ip, data.mac))
        if self.AMX_only_filter:
            if data.mac[0:8] != '00:60:9f':
                    return
        selectedItems = self.main_list.GetSelectedObjects()
        if self.main_list.GetObjects() == []:
            self.main_list.SetObjects([data])
        else:
            for obj in self.main_list.GetObjects():
                if obj.mac == data.mac:
                    obj.ip = data.ip
                    obj.hostname = data.hostname
                    obj.arrival_time = data.arrival_time
                    break
            else:
                self.main_list.AddObject(data)
        self.main_list.RepopulateList()
        self.main_list.SelectObjects(selectedItems, deselectOthers=True)
        self.dumpPickle()
        self.playSound()

    def readConfigFile(self):
        self.os_type = os.name
        if self.os_type == 'nt':
            self.path = os.path.expanduser('~\\Documents\\Magic_DXLink_Configurator\\')
        else:
            self.path = os.path.expanduser('~/Documents/Magic_DXLink_Configurator/')
        self.config = ConfigParser.RawConfigParser()
        try:  # read the settings file
            self.config.read((self.path + "settings.txt"))
            self.master_address = (self.config.get('Settings', 'default master address'))
            self.device_number = (self.config.get('Settings', 'default device number'))
            self.default_dhcp = (self.config.getboolean('Settings', 'default enable DHCP'))
            self.thread_number = (self.config.get('Settings', 'number of threads'))
            self.telnet_client = (self.config.get('Settings', 'telnet client executable'))
            self.telnet_timeout_seconds = (self.config.get('Settings', 'telnet timeout in seconds'))
            self.displaysuccess = (self.config.getboolean('Settings', 'display notification of successful connections'))
            self.dhcp_sniffing = (self.config.getboolean('Settings', 'DHCP sniffing enabled'))
            self.AMX_only_filter = (self.config.getboolean('Settings', 'filter incoming DHCP for AMX only'))
            self.play_sounds = (self.config.getboolean('Settings', 'play sounds'))
            self.columns_config = (self.config.get('Config', 'columns_config'))
        except:   # Make a new settings file, because we couldn't read the old one
            self.createConfigFile()
            self.readConfigFile()
        return

    def createConfigFile(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        try:
            #os.path.exists(self.path + 'settings.txt'):
            os.remove(self.path + 'settings.txt')
        except:
            pass
        with open((self.path + "settings.txt"), 'w') as f:
            f.write("")
        self.config = ConfigParser.RawConfigParser()
        self.config.add_section('Settings')
        self.config.set('Settings', 'default master address', '192.168.1.1')
        self.config.set('Settings', 'default device number', '10001')
        self.config.set('Settings', 'default enable dhcp', True )
        self.config.set('Settings', 'number of threads', 20 )
        self.config.set('Settings', 'telnet client executable', ('puttytel.exe'))
        self.config.set('Settings', 'telnet timeout in seconds', '4')
        self.config.set('Settings', 'display notification of successful connections', True)
        self.config.set('Settings', 'DHCP sniffing enabled', True)
        self.config.set('Settings', 'filter incoming DHCP for AMX only', True)
        self.config.set('Settings', 'play sounds', True)
        self.config.add_section('Config')
        self.config.set('Config', 'Columns are with a 1 are displayed. ', ' unless you know what your doing, please change these in the application')
        self.config.set('Config', 'columns_config', '11111111110')
        # Writing our configuration file to 'settings.txt'
        with open((self.path + "settings.txt"), 'w') as configfile:
            self.config.write(configfile)

    def writeConfigFile(self):
        self.config = ConfigParser.RawConfigParser()
        self.config.read((self.path + "settings.txt"))
        self.config.set('Settings', 'default master address', self.master_address )
        self.config.set('Settings', 'default device number', self.device_number )
        self.config.set('Settings', 'default enable dhcp', self.default_dhcp)
        self.config.set('Settings', 'number of threads', self.thread_number )
        self.config.set('Settings', 'telnet client executable', self.telnet_client)
        self.config.set('Settings', 'telnet timeout in seconds', self.telnet_timeout_seconds)
        self.config.set('Settings', 'display notification of successful connections', self.displaysuccess)
        self.config.set('Settings', 'DHCP sniffing enabled', self.dhcp_sniffing)
        self.config.set('Settings', 'filter incoming DHCP for AMX only', self.AMX_only_filter)
        self.config.set('Settings', 'play sounds', self.play_sounds)
        self.config.set('Config', 'columns_config', self.columns_config)
        with open((self.path + "settings.txt"), 'w') as configfile:
                self.config.write(configfile)

    def setTitleBar(self, data=None):
        self.parent.SetTitle(self.name + " " + self.version)

    def configureDevice( self, event):
        if len(self.main_list.GetSelectedObjects()) == 0: return
        self.staticItems = []
        self.abort = False
        for obj in self.main_list.GetSelectedObjects():
            dia = config_menus.DeviceConfig(self, obj)
            dia.ShowModal()
            dia.Destroy()
            if self.abort == True:
                #self.actionItems = []
                return
        #self.actionItems = self.staticItems
        #if self.actionItems != []:
        #    self.displayProgress()

    def configurePrefs( self, event ):
        dia = config_menus.PreferencesConfig(self)
        dia.ShowModal()
        dia.Destroy()


    def loadDataPickle(self, data=None):
        if os.path.exists((self.path + 'data_store.pkl')):
            try:
                objects = pickle.load(open((self.path + 'data_store.pkl'), 'rb'))
                self.main_list.SetObjects(objects)
            except:
                pass
        self.main_list.SetSortColumn(0, resortNow = True)

    def resizeFrame(self):
        """Resizes the Frame"""
        panel_width = 30
        for i in range(len(self.columns_config)):
            columns_width = [90,130,130,100,130,150,80,80,60,100,80]
            if self.columns_config[i] == '1':
                panel_width = panel_width + columns_width[i]
        if panel_width <  400:
            panel_width = 400
        self.parent.SetSize((panel_width,600))

    def update_status_bar(self):
        """Updates the status bar."""
        self.parent.status_bar.SetFieldsCount(4)
        master_width = wx.ClientDC(self.parent.status_bar).\
                       GetTextExtent(self.master_address)[0] + 0
        device_width = wx.ClientDC(self.parent.status_bar).\
                       GetTextExtent(self.device_number)[0] + 0
        self.parent.status_bar.SetStatusWidths([-1, master_width, \
                                                device_width, 30])
        self.parent.status_bar.SetStatusText(self.master_address, 1)
        self.parent.status_bar.SetStatusText(self.device_number, 2)

    def onClose(self, data=None):
        self.parent.Destroy()

    def OnAboutBox(self, event):

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

    def OnBeerBox(self, event):
        dlg = wx.MessageDialog(parent=self, message='If you enjoy this ' + \
                               'program \n Click Ok to Buy me a beer', \
                               caption='Buy me a beer', \
                               style=wx.OK|wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            url = 'http://ornear.com/give_a_beer'
            # Open URL in a new tab, if a browser window is already open.
            webbrowser.open_new_tab(url)
            # Open URL in new window, raising the window if possible.
            #webbrowser.open_new(url)
        dlg.Destroy()


########################################################################
class MainFrame(wx.Frame):
    #----------------------------------------------------------------------
    def __init__(self):

        self.title_text = "Starting up"
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, 
                          title=self.title_text, size=(1100, 600))

        _ib = wx.IconBundle()
        _ib.AddIconFromFile(r"icon\MDC_icon.ico", wx.BITMAP_TYPE_ANY)
        self.SetIcons(_ib)
        #self.SetIcon(icon.MDC_icon.GetIcon())

        menubar = wx.MenuBar()
        self.status_bar = self.CreateStatusBar()

        self.panel = MainPanel(self)

        file_menu = wx.Menu()
        fitem = file_menu.Append(wx.ID_ANY, 'Import CSV Spread Sheet', \
                                 'Import CSV Spread Sheet')
        self.Bind(wx.EVT_MENU, self.panel.importCSVfile, fitem)

        fitem = file_menu.Append(wx.ID_ANY, 'Import IP list', 'Import IP list')
        self.Bind(wx.EVT_MENU, self.panel.importIPlist, fitem)

        fitem = file_menu.Append(wx.ID_ANY, 'Import Plot', 'Import Plot')
        self.Bind(wx.EVT_MENU, self.panel.importPlot, fitem)

        fitem = file_menu.Append(wx.ID_ANY, 'Store Items in a CSV File', \
                                 'Store selected items in a CSV file')
        self.Bind(wx.EVT_MENU, self.panel.removeAndStore, fitem)

        fitem = file_menu.Append(wx.ID_EXIT, '&Quit', 'Quit application')
        self.Bind(wx.EVT_MENU, self.onQuit, fitem)

        menubar.Append(file_menu, '&File')

        edit_menu = wx.Menu()

        select_menu = wx.Menu()
        sitem = select_menu.Append(wx.ID_ANY, 'Select All', 'Select All')
        self.Bind(wx.EVT_MENU, self.panel.onSelectAll, sitem)

        sitem = select_menu.Append(wx.ID_ANY, 'Select None', 'Select None')
        self.Bind(wx.EVT_MENU, self.panel.onSelectNone, sitem)

        menubar.Append(edit_menu, '&Edit')
        edit_menu.AppendMenu(wx.ID_ANY, 'Select', select_menu)

        eitem = edit_menu.Append(wx.ID_ANY, 'Preferences', 'Preferences')
        self.Bind(wx.EVT_MENU, self.panel.configurePrefs, eitem)

        action_menu = wx.Menu()

        aitem = action_menu.Append(wx.ID_ANY, 'Update device information', \
                                   'Update details from selected devices')
        self.Bind(wx.EVT_MENU, self.panel.getTelnetInfo, aitem)

        aitem = action_menu.Append(wx.ID_ANY, 'Configure Device', \
                                   'Configure Devices Connection')
        self.Bind(wx.EVT_MENU, self.panel.configureDevice, aitem)

        aitem = action_menu.Append(wx.ID_ANY, 'Send Commands', 'Send Commands')
        self.Bind(wx.EVT_MENU, self.panel.sendCommands, aitem)

        aitem = action_menu.Append(wx.ID_ANY, 'Reset Factory', \
                                   'Reset selected devices to factory settings')
        self.Bind(wx.EVT_MENU, self.panel.resetFactory, aitem)

        aitem = action_menu.Append(wx.ID_ANY, 'Reboot Unit', \
                                   'Reboot selected devices')
        self.Bind(wx.EVT_MENU, self.panel.rebootUnit, aitem)

        menubar.Append(action_menu, '&Actions')

        tools_menu = wx.Menu()

        titem = tools_menu.Append(wx.ID_ANY, 'Ping devices', 'Ping devices')
        self.Bind(wx.EVT_MENU, self.panel.multiPing, titem)

        titem = tools_menu.Append(wx.ID_ANY, 'Add a line item', 'Add a line')
        self.Bind(wx.EVT_MENU, self.panel.addLine, titem)

        titem = tools_menu.Append(wx.ID_ANY, 'Generate IP List', \
                                  'Generate IP List')
        self.Bind(wx.EVT_MENU, self.panel.generateList, titem)

        titem = tools_menu.Append(wx.ID_ANY, 'Turn on LED\'s', 'Turn on LED')
        self.Bind(wx.EVT_MENU, self.panel.turnOnLED, titem)

        titem = tools_menu.Append(wx.ID_ANY, 'Turn off LED\'s', 'Turn off LED')
        self.Bind(wx.EVT_MENU, self.panel.turnOffLED, titem)

        menubar.Append(tools_menu, 'Tools')

        listen_menu = wx.Menu()


        self.listen_dhcp = listen_menu.AppendCheckItem(wx.ID_ANY, \
                                                   "Listen for DHCP requests", \
                                                   "Listen for DHCP requests")

        self.Bind(wx.EVT_MENU, self.panel.toggleDHCPsniffing, self.listen_dhcp)
        self.listen_dhcp.Check(self.panel.dhcp_sniffing)

        self.listen_filter = listen_menu.AppendCheckItem(wx.ID_ANY, \
                                           "Filter AMX devices DHCP requests", \
                                           "Filter AMX devices DHCP requests")

        self.Bind(wx.EVT_MENU, self.panel.togglefilterAMX, self.listen_filter)
        self.listen_filter.Check(self.panel.AMX_only_filter)

        menubar.Append(listen_menu, 'Listen')

        delete_menu = wx.Menu()
        ditem = delete_menu.Append(wx.ID_ANY, '&Delete Item', 'Delete Item')
        self.Bind(wx.EVT_MENU, self.panel.deleteItem, ditem)

        ditem = delete_menu.Append(wx.ID_ANY, '&Delete All Items', \
                                   'Delete All Items')
        self.Bind(wx.EVT_MENU, self.panel.deleteAllItems, ditem)

        menubar.Append(delete_menu, '&Delete')

        help_menu = wx.Menu()
        hitem = help_menu.Append(wx.ID_ANY, 'About', 'About')
        self.Bind(wx.EVT_MENU, self.panel.OnAboutBox, hitem)

        hitem = help_menu.Append(wx.ID_ANY, 'Beer', 'Beer')
        self.Bind(wx.EVT_MENU, self.panel.OnBeerBox, hitem)

        menubar.Append(help_menu, '&Help')

        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_CLOSE, self.panel.onClose)

        if self.panel.port_error:
            self.panel.portErrors()

    def onRightClick(self, event):

        rc_menu = wx.Menu()

        rcitem = rc_menu.Append(wx.ID_ANY, 'Update device information')
        self.Bind(wx.EVT_MENU, self.panel.getTelnetInfo, rcitem)

        rcitem = rc_menu.Append(wx.ID_ANY, 'Configure Device')
        self.Bind(wx.EVT_MENU, self.panel.configureDevice, rcitem)

        rcitem = rc_menu.Append(wx.ID_ANY, 'Send Commands')
        self.Bind(wx.EVT_MENU, self.panel.sendCommands, rcitem)

        rcitem = rc_menu.Append(wx.ID_ANY, 'Reset Factory')
        self.Bind(wx.EVT_MENU, self.panel.resetFactory, rcitem)

        rcitem = rc_menu.Append(wx.ID_ANY, 'Delete')
        self.Bind(wx.EVT_MENU, self.panel.deleteItem, rcitem)

        rcitem = rc_menu.Append(wx.ID_ANY, 'Telnet to Device')
        self.Bind(wx.EVT_MENU, self.panel.telnetTo, rcitem)

        rcitem = rc_menu.Append(wx.ID_ANY, 'FactoryAV')
        self.Bind(wx.EVT_MENU, self.panel.factoryAV, rcitem)

        rcitem = rc_menu.Append(wx.ID_ANY, 'Reboot Device')
        self.Bind(wx.EVT_MENU, self.panel.rebootUnit, rcitem)

        rcitem = rc_menu.Append(wx.ID_ANY, 'Plot MSE')
        self.Bind(wx.EVT_MENU, self.panel.plotMSE, rcitem)

        rcitem = rc_menu.Append(wx.ID_ANY, 'Open device in webbrowser')
        self.Bind(wx.EVT_MENU, self.panel.openURL, rcitem)

        self.PopupMenu(rc_menu)
        rc_menu.Destroy()

    def onQuit(self, event):
        self.panel.dumpPickle()
        self.Close()


########################################################################
class GenApp(wx.App):

    #----------------------------------------------------------------------
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)

    #----------------------------------------------------------------------
    def OnInit(self):
        # create frame here
        frame = MainFrame()
        frame.Show()
        return True

#----------------------------------------------------------------------
def main():

    app = GenApp()
    app.MainLoop()

# Run the program
if __name__ == "__main__":
    main()
