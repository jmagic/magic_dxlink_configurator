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

from scripts import *

try:
    import winsound
except:
    pass



########################################################################
class Unit(object):
    """
    Model of the Unit

    Contains the following attributes:
    model, hostname, serial ,firmware, device, mac, ip, time, ip_type, gateway, subnet, master, system
    """
    #----------------------------------------------------------------------
    def __init__(self, model, hostname, serial ,firmware, device, mac, ip, time, ip_type, gateway, subnet, master, system):

        self.model = model
        self.hostname = hostname
        self.serial = serial
        self.firmware = firmware
        self.device = device
        self.mac = mac
        self.ip = ip
        self.time = time
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
        self.version = "v1.5.0"
        self.setTitleBar()

        # Set up some variables
        #self.AMX_only_filter = False #disable the AMX filter by default
        self.errorlist = []
        self.completionlist = []
        self.mse_active_list = []

        # Build the ObjectListView
        self.dataOlv = ObjectListView(self, wx.ID_ANY, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.dataOlv.cellEditMode = ObjectListView.CELLEDIT_DOUBLECLICK
        self.dataOlv.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, parent.onRightClick)
        self.dataOlv.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)

        # Select columns displayed
        self.columns = []

        self.columns_setup = [  ColumnDefn("Time", "center", 90, "time",
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
        self.updateStatusBar()

        # Create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.dataOlv, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(mainSizer)

        # Create DHCP listening thread
        self.SniffDHCPThread = dhcp_sniffer.SniffDHCPThread(self)
        self.SniffDHCPThread.setDaemon(True)
        self.SniffDHCPThread.start()
        self.DHCPListenerRunning = True

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
        self.parent.listenfilter.Enable(self.AMX_only_filter)
        self.parent.listenDHCP.Enable(False)
        self.DHCPListenerRunning = False


    def displayProgress(self, data=None):
        total = len(self.actionItems)
        if total == 1:

            dlg = wx.ProgressDialog("Attempting connect to selected device",
                                    'Attempting connection to selected device',
                                    maximum = total,
                                    parent = self.parent,
                                    style =  wx.PD_APP_MODAL
                                     | wx.PD_AUTO_HIDE
                                     | wx.PD_SMOOTH
                                     #| wx.PD_ELAPSED_TIME
                                     )

            while ((len(self.completionlist) + len(self.errorlist)) < total):
                count = (len(self.completionlist) + len(self.errorlist))
                time.sleep(.01)
                dlg.Pulse()
        else:
            dlg = wx.ProgressDialog("Attempting connect to selected devices",'Attempting connection to all selected devices',
                                maximum = total,
                                parent = self.parent,
                                style =  wx.PD_APP_MODAL
                                 | wx.PD_AUTO_HIDE
                                 | wx.PD_SMOOTH
                                 | wx.PD_ELAPSED_TIME
                                 )

            while ((len(self.completionlist) + len(self.errorlist)) < total):
                count = (len(self.completionlist) + len(self.errorlist))
                dlg.Update (count,"Attempting connection to %s of %s devices" % ((count + 1),total))

        dlg.Destroy()
        self.dataOlv.RefreshObjects(self.actionItems)
        self.dumpPickle()

        errortext = ""
        phil =" "
        #print self.errorlist
        for i in xrange(len(self.errorlist)):
            while (len(self.errorlist[i][0]) + (len(phil) - 1)) < 15:
                phil = phil + " "
            errortext = errortext + self.errorlist[i][0] + " " + phil + " " +  self.errorlist[i][1] + "\n"
            phil = " "

        completiontext = ""
        for i in xrange(len(self.completionlist)):
            completiontext = completiontext + self.completionlist[i][0] + "\n"
        #print errortext
        if (len(self.errorlist) == len(self.actionItems)):
            dlg = wx.MessageDialog(parent=self,
                                   message= 'Failed to connect to \n======================= \n%s ' % errortext ,
                                   caption = 'Failed connection list',
                                   style = wx.OK
                                   )
            dlg.ShowModal()
            dlg.Destroy()

        elif (len(self.completionlist) == len(self.actionItems)):
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

        self.dataOlv.RefreshObjects(self.actionItems)
        self.dumpPickle()
        self.errorlist = []
        self.completionlist = []
        self.actionItems = []
        self.singleSelect = []


    def DHCPListen(self, data=None):

        if self.DHCPListenerRunning == True:
            dispatcher.send( signal="start_stop_dhcp", sender="stop" )
            self.DHCPListenerRunning = False

        else:
            self.parent.sb.SetStatusText('Listening for DHCP requests')
            dispatcher.send( signal="start_stop_dhcp", sender="start" )
            self.DHCPListenerRunning = True


    def selectColumns(self):

        self.columns = []
        for i in range(len(self.columns_setup)):
            self.columns.append((int(self.columns_config[i]),self.columns_setup[i]))

        todisplay = []
        for item in self.columns:
            if item[0] == 1:

                todisplay.append(item[1])

        self.dataOlv.SetColumns(todisplay)


    def setClients(self, objects):

        if self.AMX_only_filter:
            filterclients = []
            for obj in objects:
                if obj.mac[0:8] == '00:60:9f':
                    filterclients.append(obj)
            self.dataOlv.SetObjects(filterclients)

        else:
            self.dataOlv.SetObjects(objects)


    def getRowInfo(self):

        self.actionItems = self.dataOlv.GetSelectedObjects()

        if self.actionItems == []:


            dlg = wx.MessageDialog(parent=self, message= 'Nothing selected.... \nPlease click on the device you want to select',
                                   caption = 'Nothing Selected',
                                   style = wx.OK
                                   )
            dlg.ShowModal()
            dlg.Destroy()

    def onSelectAll(self, data=None):

        objects = self.dataOlv.GetObjects()
        self.dataOlv.SelectAll()
        self.dataOlv.RefreshObjects(objects)


    def onSelectNone(self, data=None):

        objects = self.dataOlv.GetObjects()
        self.dataOlv.DeselectAll()
        self.dataOlv.RefreshObjects(objects)


    def telnetTo( self, data=None ):

        self.getRowInfo()
        if len(self.actionItems) == 0:return
        if len(self.actionItems) > 10:
            dlg = wx.MessageDialog(parent=self, message= 'I can only telnet to 10 devices at a time \nPlease select less than ten devices at once',
                                   caption = 'How many telnets?',
                                   style = wx.OK
                                   )
            dlg.ShowModal()
            dlg.Destroy()
            return
        if self.os_type == 'nt':
            if os.path.exists((self.path + self.telnet_client)):

                for obj in self.actionItems:
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
            for obj in self.actionItems:
                self.telnettoqueue.put(obj)

    def plotMSE(self, data=None):

        self.getRowInfo()
        if len(self.actionItems) == 0:return
        if len(self.actionItems) > 10:
            dlg = wx.MessageDialog(parent=self, message= 'I can only graph 10 devices at a time \nPlease select less than ten devices at once',
                                   caption = 'How many graphs?',
                                   style = wx.OK
                                   )
            dlg.ShowModal()
            dlg.Destroy()
            return

        for obj in self.actionItems:
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

        self.actionItems = []


    def factoryAV(self, data=None):

        self.getRowInfo()
        if len(self.actionItems) == 0: return

        for obj in self.actionItems:
            self.telnetjobqueue.put(['FactoryAV', obj, self.telnet_timeout_seconds, 'FACTORYAV', 1])
        self.displayProgress()


    def resetFactory(self, data=None ):

        self.getRowInfo()
        if len(self.actionItems) == 0: return

        for obj in self.actionItems:

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


    def rebootUnit(self, data=None ):

        self.getRowInfo()
        if len(self.actionItems) == 0: return

        for obj in self.actionItems:

            self.telnetjobqueue.put(['SetReboot', obj, self.telnet_timeout_seconds])

        self.displayProgress()


    def openURL(self, data= None):

        self.getRowInfo()
        if len(self.actionItems) == 0: return

        for obj in self.actionItems:
            url = 'http://' + obj.ip
            # Open URL in a new tab, if a browser window is already open.
            webbrowser.open_new_tab(url)


    def getTelnetInfo( self, data=None):

        self.getRowInfo()
        if len(self.actionItems) == 0: return

        for obj in self.actionItems:
            self.telnetjobqueue.put(['GetTelnetInfo', obj,  self.telnet_timeout_seconds])

        self.displayProgress()

    def turnOnLED(self, data= None):

        self.getRowInfo()
        if len(self.actionItems) == 0: return

        for obj in self.actionItems:
            self.telnetjobqueue.put(['TurnOnLED', obj,  self.telnet_timeout_seconds])

        self.displayProgress()

    def turnOffLED(self, data= None):

        self.getRowInfo()
        if len(self.actionItems) == 0: return

        for obj in self.actionItems:
            self.telnetjobqueue.put(['TurnOffLED', obj,  self.telnet_timeout_seconds])

        self.displayProgress()

    def sendCommands(self, data=None):

        self.getRowInfo()
        if len(self.actionItems) == 0: return


        self.tx_devices = []
        self.rx_devices = []

        for obj in self.actionItems:
            #self.telnetjobqueue.put(['getTelnetInfo', obj,  self.telnet_timeout_seconds])

            if obj.model[12:14] == 'TX' or obj.model[12:14] == 'WP'or obj.model[12:15] == 'DWP'or obj.model[12:16] == 'MFTX':
                self.tx_devices.append(obj)
            elif obj.model[12:14] == 'RX':
                self.rx_devices.append(obj)
            else:
                pass
        #self.displayProgress()

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
        #data = []
        objects = self.dataOlv.GetObjects()
        #for obj in objects:
        #    client = [obj.model,
        #              obj.hostname,
        #              obj.serial,
        #              obj.firmware,
        #              obj.device,
        #              obj.mac,
        #              obj.ip,
        #              obj.time,
        #              obj.ip_type,
        #              obj.gateway,
        #              obj.subnet,
        #              obj.master,
        #              obj.system
        #              ]

        #   data.append(client)
        pickle.dump(objects, open((self.path + 'data.pkl') , 'wb'))


    def removeAndStore( self, data=None ):

        self.getRowInfo()

        total = len(self.actionItems)
        if total == 0:
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
                                    maximum = total,
                                    parent = self,
                                    style =  wx.PD_APP_MODAL
                                     | wx.PD_AUTO_HIDE
                                     #| wx.PD_CAN_ABORT
                                     | wx.PD_ELAPSED_TIME
                                     )
            count = 0
            f = open( path ,'a')
            for obj in self.actionItems:
                count += 1
                dlg.Update(count)

                data = [obj.model,
                        obj.hostname,
                        obj.serial,
                        obj.firmware,
                        obj.device,
                        obj.mac,
                        obj.ip,
                        obj.time,
                        obj.ip_type,
                        obj.gateway,
                        obj.subnet,
                        obj.master,
                        obj.system
                        ]

                w = csv.writer(f, quoting=csv.QUOTE_ALL)
                w.writerow(data)

                self.dataOlv.RemoveObject(obj)
                #self.clients.remove(obj)

            f.close()
            self.dataOlv.RepopulateList()
            self.dumpPickle()


    def importCSVfile( self, data=None ):

        openFileDialog = wx.FileDialog(
                       self, message="Import a CSV file",
                       defaultDir=self.path,
                       defaultFile= "",
                       wildcard="CSV files (*.csv)|*.csv",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_OK:

            path = openFileDialog.GetPath()
            openFileDialog.Destroy()
            #self.clients = []
            self.dataOlv.DeleteAllItems()
            objects = []
            with open( path ,'rb') as csvfile:
                cvs_data = csv.reader(csvfile)
                for item in cvs_data:
                    data = [Unit(
                         item[0],
                         item[1],
                         item[2],
                         item[3],
                         item[4],
                         item[5],
                         item[6],
                         datetime.datetime.strptime((item[7]),"%Y-%m-%d %H:%M:%S.%f"),
                         item[8],
                         item[9],
                         item[10],
                         item[11],
                         item[12]
                        )
                    ]
                    objects.append(data[0])


            #self.clients = objects
            #print type(self.clients[0].time)
            self.dataOlv.SetObjects(objects)
            self.dumpPickle()
        else:
            openFileDialog.Destroy()

    def importPlot(self, data=None):

        openFileDialog = wx.FileDialog(
                       self, message="Import a plot CSV file",
                       defaultDir=self.path,
                       defaultFile= "",
                       wildcard="CSV files (*.csv)|*.csv",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_OK:

            path = openFileDialog.GetPath()
            openFileDialog.Destroy()

            with open( path ,'rb') as csvfile:
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

                row_count = (sum(1 for row in csv_data)-1)*-1

                dia = plot_class.Multi_Plot(self, obj, row_count)
                dia.Show()
            with open( path ,'rb') as csvfile:  # opening it again to start at top
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

    def importIPlist(self, data=None):

        #self.clients = []

        openFileDialog = wx.FileDialog(
                       self, message="Open IP List",
                       defaultDir=self.path,
                       defaultFile= "",
                       wildcard="CSV files (*.csv)|*.csv",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_OK:
            path = openFileDialog.GetPath()
            self.dataOlv.DeleteAllItems()
            objects = []
            with open(path,'rb') as csvfile:
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


                    objects.append(data)

            #self.clients = objects

            self.dataOlv.SetObjects(objects)
            self.dumpPickle()
            openFileDialog.Destroy()

        else:
            openFileDialog.Destroy()


    def generateList(self, data=None):

        dia = config_menus.IpListGen(self)
        dia.ShowModal()
        dia.Destroy()

    def addLine(self, data=None):

        data =  [Unit(
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
                ]

        objects = self.dataOlv.GetObjects()
        objects.append(data[0])

        #self.clients = objects
        self.dataOlv.SetObjects(objects)
        self.dataOlv.RepopulateList()
        self.dumpPickle()


    def deleteItem(self, data=None):

        self.getRowInfo()
        total = len(self.actionItems)
        if total == len(self.dataOlv.GetObjects()):
            self.dataOlv.DeleteAllItems()
            self.dumpPickle()
            return
        if total == 0:
            return

        dlg = wx.ProgressDialog("Deleting Items","Deleting Items",
                                    maximum = total,
                                    parent = self,
                                    style =  wx.PD_APP_MODAL
                                     | wx.PD_AUTO_HIDE
                                     #| wx.PD_CAN_ABORT
                                     | wx.PD_ELAPSED_TIME
                                     )
        count = 0

        #for obj in self.actionItems:
        unselected = []
        for obj in self.dataOlv.GetObjects():

            if obj not in self.actionItems:

                unselected.append(obj)
            else:
                count +=1
                dlg.Update(count)
        #if len(self.actionItems) >= len(unselected):
        self.dataOlv.DeleteAllItems()
        self.dataOlv.SetObjects(unselected)
        #else:
        ##   self.dataOlv.SetObjects(self.actionItems)



            #count += 1
            #dlg.Update(count)

            #self.dataOlv.RemoveObject(obj)

        self.dataOlv.RepopulateList()
        self.dumpPickle()


    def deleteAllItems(self, data=None):

        dlg = wx.MessageDialog(parent=self, message= 'Are you sure? \n This will delete all items in the list',
                                   caption = 'Delete All Items',
                                   style = wx.OK|wx.CANCEL
                                   )

        if dlg.ShowModal() == wx.ID_OK:

            self.dataOlv.DeleteAllItems()
            self.dumpPickle()
        else:
            return


    def filterAMX(self, data=None):
        if self.AMX_only_filter == True:
            self.AMX_only_filter = False
        else:
            self.AMX_only_filter = True

    def makeUnit(self, sender):

        data = Unit(    '',
                        sender['hostname'],
                        '',
                        '',
                        '',
                        sender['mac'],
                        sender['ip'],
                        sender['time'],
                        '',
                        '',
                        '',
                        '',
                        ''
                    )


        '''Unit(sender['model'],
                     sender['hostname'],
                     sender['serial'],
                     sender['firmware'],
                     sender['device'],
                     sender['mac'],
                     sender['ip'],
                     sender['time'],
                     sender['ip_type'],
                     sender['gateway'],
                     sender['subnet'],
                     sender['master'],
                     sender['system']
                    )
        '''
        return(data)


    def updateInfo(self, sender):
        """
        Receives dhcp requests with and adds them to objects to display
        """
        data = self.makeUnit(sender)

        objects = self.dataOlv.GetObjects()
        last_time = data.time.strftime('%I:%M%p')
        self.parent.sb.SetStatusText('%s -- %s %s %s' %(last_time,  data.hostname, data.ip, data.mac))

        if self.AMX_only_filter:
            if data.mac[0:8] != '00:60:9f':
                    return

        selectedItems = self.dataOlv.GetSelectedObjects()
        #self.getRowInfo()
        #isSelected = False
        for obj in objects:
            if obj.mac == data.mac:
                data.model = obj.model
                data.serial = obj.serial
                data.firmware = obj.firmware
                data.device = obj.device
                data.ip_type = obj.ip_type
                data.gateway = obj.gateway
                data.subnet = obj.subnet
                data.master = obj.master
                data.system = obj.system


                self.dataOlv.RemoveObject(obj)


        objects = self.dataOlv.GetObjects()
        objects.append(data)

        #self.clients = objects
        self.dataOlv.SetObjects(objects)
        for obj in selectedItems:
            if data.mac == obj.mac:

                selectedItems.remove(obj)
                selectedItems.append(data)
                self.dataOlv.SelectObjects(selectedItems, deselectOthers=True)

        #self.flashObject(data, selectedItems)

        self.dataOlv.SelectObjects(selectedItems, deselectOthers=True)

        self.dumpPickle()
        self.playSound()

    def flashObject(self, obj, selected):
        print "selected: " + str(selected)
        print 'obj ' + str(obj)

        selected_all =  self.dataOlv.GetSelectedObjects()
        selected.remove(obj)
        print "selected: " + str(selected)
        print "selected_all: " + str(selected_all)
        print 'obj ' + str(obj)
        if obj in selected_all:
            print 'in selected'

            self.dataOlv.SelectObjects(selected, deselectOthers=True)
            time.sleep(1)
            self.dataOlv.SelectObjects(selected_all, deselectOthers=True)
            time.sleep(1)
            self.dataOlv.SelectObjects(selected, deselectOthers=True)
            time.sleep(1)
            print 'done'


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
            self.dhcp = (self.config.getboolean('Settings', 'default enable DHCP'))
            self.thread_number = (self.config.get('Settings', 'number of threads'))
            self.telnet_client = (self.config.get('Settings', 'telnet client executable'))
            self.telnet_timeout_seconds = (self.config.get('Settings', 'telnet timeout in seconds'))
            self.displaysuccess = (self.config.getboolean('Settings', 'display notification of successful connections'))
            self.listen_dhcp_enable = (self.config.getboolean('Settings', 'DHCP sniffing enabled'))
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
        self.config.set('Settings', 'default enable dhcp', self.dhcp)
        self.config.set('Settings', 'number of threads', self.thread_number )
        self.config.set('Settings', 'telnet client executable', self.telnet_client)
        self.config.set('Settings', 'telnet timeout in seconds', self.telnet_timeout_seconds)
        self.config.set('Settings', 'display notification of successful connections', self.displaysuccess)
        self.config.set('Settings', 'DHCP sniffing enabled', self.dhcp)
        self.config.set('Settings', 'filter incoming DHCP for AMX only', self.AMX_only_filter)
        self.config.set('Settings', 'play sounds', self.play_sounds)
        self.config.set('Config', 'columns_config', self.columns_config)

        with open((self.path + "settings.txt"), 'w') as configfile:
                self.config.write(configfile)
        #print self.columns_config

    def setTitleBar(self, data=None):
        self.parent.SetTitle(self.name + " " + self.version)
        #+ "           Default Master address: " + self.master_address + "     Default Device Number: " + str(self.device_number))


    def configureDevice( self, data=None ):

        self.getRowInfo()
        if len(self.actionItems) == 0: return

        self.staticItems = []
        self.abort = False
        for obj in self.actionItems:
            dia = config_menus.DeviceConfig(self, obj)
            dia.ShowModal()
            dia.Destroy()
            if self.abort == True:
                self.actionItems = []
                return
        self.actionItems = self.staticItems
        if self.actionItems != []:
            self.displayProgress()


    def configurePrefs( self, data=None ):

        dia = config_menus.PreferencesConfig(self)
        dia.ShowModal()
        dia.Destroy()


    def loadDataPickle(self, data=None):

        if os.path.exists((self.path + 'data.pkl')):
            try:
                objects = pickle.load(open((self.path + 'data.pkl'), 'rb'))
                self.dataOlv.SetObjects(objects)

            except:

                pass
        #else:
        #    #self.clients = []
        #    #self.setClients(objects)
        #    pass
        self.dataOlv.SetSortColumn(0, resortNow = True)

    def resizeFrame(self):

        panel_width = 30
        for i in range(len(self.columns_config)):
            columns_width = [90,130,130,100,130,150,80,80,60,100,80]

            if self.columns_config[i] == '1':
                panel_width = panel_width + columns_width[i]

        if panel_width <  400:
            panel_width = 400
        self.parent.SetSize((panel_width,600))

    def updateStatusBar(self):

        self.parent.sb.SetFieldsCount(4)
        master_width = wx.ClientDC(self.parent.sb).GetTextExtent(self.master_address)[0] + 0
        device_width = wx.ClientDC(self.parent.sb).GetTextExtent(self.device_number)[0] + 0
        self.parent.sb.SetStatusWidths([-1,master_width,device_width,30])
        self.parent.sb.SetStatusText(self.master_address,1)
        self.parent.sb.SetStatusText(self.device_number,2)

    def onClose(self, data=None):
        self.parent.Destroy()

    def OnAboutBox(self, e):

        description = """Magic DXLink Configurator is an tool for configuring
DXLINK Devices. Features include a DHCP monitor,
import and export csv files, batch ip listing,
serial number extraction, reboots and more.
"""

        licence = """Magic DXLink Configurator is distributed in the hope
that it will be useful, but WITHOUT ANY WARRANTY.
"""

        info = wx.AboutDialogInfo()

        info.SetName(self.name)
        info.SetVersion(self.version)
        info.SetDescription(description)

        info.SetLicence(licence)
        info.AddDeveloper('Jim Maciejewski')

        wx.AboutBox(info)

    def OnBeerBox(self, e):

        dlg = wx.MessageDialog(parent=self, message= 'If you enjoy this program \nBuy me a beer',
                                       caption = 'Buy me a beer',
                                       style = wx.OK|wx.CANCEL
                                       )
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
                          title=self.title_text, size=(1100,600))

        self.SetIcon(icon.MDC_icon.GetIcon())

        menubar = wx.MenuBar()
        self.sb = self.CreateStatusBar()

        self.panel = MainPanel(self)

        fileMenu = wx.Menu()
        fitem =  fileMenu.Append(wx.ID_ANY, 'Import CSV Spread Sheet', 'Import CSV Spread Sheet')
        self.Bind(wx.EVT_MENU, self.panel.importCSVfile, fitem)

        fitem =  fileMenu.Append(wx.ID_ANY, 'Import IP list','Import IP list')
        self.Bind(wx.EVT_MENU, self.panel.importIPlist, fitem)

        fitem =  fileMenu.Append(wx.ID_ANY, 'Import Plot','Import Plot')
        self.Bind(wx.EVT_MENU, self.panel.importPlot, fitem)

        fitem = fileMenu.Append(wx.ID_ANY, 'Store Items in a CSV File','Store selected items in a CSV file')
        self.Bind(wx.EVT_MENU, self.panel.removeAndStore, fitem)

        fitem = fileMenu.Append(wx.ID_EXIT, '&Quit', 'Quit application')
        self.Bind(wx.EVT_MENU, self.onQuit, fitem)

        menubar.Append(fileMenu, '&File')

        editMenu = wx.Menu()

        selectMenu = wx.Menu()
        sitem = selectMenu.Append(wx.ID_ANY, 'Select All', 'Select All')
        self.Bind(wx.EVT_MENU, self.panel.onSelectAll, sitem)

        sitem = selectMenu.Append(wx.ID_ANY, 'Select None', 'Select None')
        self.Bind(wx.EVT_MENU, self.panel.onSelectNone, sitem)

        menubar.Append(editMenu, '&Edit')
        editMenu.AppendMenu(wx.ID_ANY, 'Select', selectMenu)

        eitem = editMenu.Append(wx.ID_ANY, 'Preferences', 'Preferences')
        self.Bind(wx.EVT_MENU, self.panel.configurePrefs, eitem)

        actionMenu = wx.Menu()

        aitem = actionMenu.Append(wx.ID_ANY, 'Update device information', 'Update details from selected devices')
        self.Bind(wx.EVT_MENU, self.panel.getTelnetInfo, aitem)

        aitem = actionMenu.Append(wx.ID_ANY, 'Send Commands', 'Send Commands')
        self.Bind(wx.EVT_MENU, self.panel.sendCommands, aitem)

        aitem = actionMenu.Append(wx.ID_ANY, 'Configure Items', 'Configure Items Connection')
        self.Bind(wx.EVT_MENU, self.panel.configureDevice, aitem)

        aitem = actionMenu.Append(wx.ID_ANY, 'Reset Factory Settings', 'Reset selected devices to factory settings')
        self.Bind(wx.EVT_MENU, self.panel.resetFactory, aitem)

        aitem = actionMenu.Append(wx.ID_ANY, 'Reboot Unit', 'Reboot selected devices')
        self.Bind(wx.EVT_MENU, self.panel.rebootUnit, aitem)

        menubar.Append(actionMenu, '&Actions')

        toolsMenu = wx.Menu()

        titem = toolsMenu.Append(wx.ID_ANY, 'Add a line item', 'Add a line')
        self.Bind(wx.EVT_MENU, self.panel.addLine, titem)

        titem = toolsMenu.Append(wx.ID_ANY, 'Generate IP List', 'Generate IP List')
        self.Bind(wx.EVT_MENU, self.panel.generateList, titem)

        titem = toolsMenu.Append(wx.ID_ANY, 'Turn on LED\'s', 'Turn on LED')
        self.Bind(wx.EVT_MENU, self.panel.turnOnLED, titem)

        titem = toolsMenu.Append(wx.ID_ANY, 'Turn off LED\'s', 'Turn off LED')
        self.Bind(wx.EVT_MENU, self.panel.turnOffLED, titem)

        menubar.Append(toolsMenu, 'Tools')

        listenMenu = wx.Menu()


        self.listenDHCP = listenMenu.AppendCheckItem(wx.ID_ANY, "Listen for DHCP requests", "Listen for DHCP requests")

        self.Bind(wx.EVT_MENU, self.panel.DHCPListen, self.listenDHCP)
        self.listenDHCP.Check(self.panel.dhcp)
        print self.panel.dhcp

        self.listenfilter = listenMenu.AppendCheckItem(wx.ID_ANY, "Filter AMX devices DHCP requests", "Filter AMX devices DHCP requests")

        self.Bind(wx.EVT_MENU, self.panel.filterAMX, self.listenfilter)
        self.listenfilter.Check(self.panel.AMX_only_filter)
        print self.panel.AMX_only_filter

        menubar.Append(listenMenu, 'Listen')

        deleteMenu = wx.Menu()
        ditem = deleteMenu.Append(wx.ID_ANY, '&Delete Item', 'Delete Item')
        self.Bind(wx.EVT_MENU, self.panel.deleteItem, ditem)

        ditem = deleteMenu.Append(wx.ID_ANY, '&Delete All Items', 'Delete All Items')
        self.Bind(wx.EVT_MENU, self.panel.deleteAllItems, ditem)

        menubar.Append(deleteMenu, '&Delete')

        helpMenu = wx.Menu()
        hitem = helpMenu.Append(wx.ID_ANY, 'About', 'About')
        self.Bind(wx.EVT_MENU, self.panel.OnAboutBox, hitem)

        hitem = helpMenu.Append(wx.ID_ANY, 'Beer', 'Beer')
        self.Bind(wx.EVT_MENU, self.panel.OnBeerBox, hitem)

        menubar.Append(helpMenu, '&Help')

        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_CLOSE, self.panel.onClose)

        #if self.panel.portError:
        #    self.panel.portErrors()

    def onRightClick(self, event):

        right_click_Menu = wx.Menu()

        rcitem = right_click_Menu.Append(wx.ID_ANY, 'Update Info', 'Update Info')
        self.Bind(wx.EVT_MENU, self.panel.getTelnetInfo, rcitem)

        rcitem = right_click_Menu.Append(wx.ID_ANY, 'Configure Item', 'Configure Item')
        self.Bind(wx.EVT_MENU, self.panel.configureDevice, rcitem)

        rcitem = right_click_Menu.Append(wx.ID_ANY, 'Send Commands', 'Send Commands')
        self.Bind(wx.EVT_MENU, self.panel.sendCommands, rcitem)

        rcitem = right_click_Menu.Append(wx.ID_ANY, 'Reset Factory', 'Reset Factory')
        self.Bind(wx.EVT_MENU, self.panel.resetFactory, rcitem)

        rcitem = right_click_Menu.Append(wx.ID_ANY, 'Delete Item', 'Delete Item')
        self.Bind(wx.EVT_MENU, self.panel.deleteItem, rcitem)

        rcitem = right_click_Menu.Append(wx.ID_ANY, 'Telnet', 'Telnet to this device')
        self.Bind(wx.EVT_MENU, self.panel.telnetTo, rcitem)

        rcitem = right_click_Menu.Append(wx.ID_ANY, 'FactoryAV', 'FactoryAV')
        self.Bind(wx.EVT_MENU, self.panel.factoryAV, rcitem)

        rcitem = right_click_Menu.Append(wx.ID_ANY, 'Reboot Unit', 'Reboot Unit device')
        self.Bind(wx.EVT_MENU, self.panel.rebootUnit, rcitem)

        rcitem = right_click_Menu.Append(wx.ID_ANY, 'Plot MSE', 'Plot MSE values')
        self.Bind(wx.EVT_MENU, self.panel.plotMSE, rcitem)

        rcitem = right_click_Menu.Append(wx.ID_ANY, 'Open as URL', 'Open Device as webpage')
        self.Bind(wx.EVT_MENU, self.panel.openURL, rcitem)

        self.PopupMenu(right_click_Menu)
        right_click_Menu.Destroy()

    def onQuit(self, e):
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
