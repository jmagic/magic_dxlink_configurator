"""Continuously pings devices for troubleshooting"""

import wx
from pydispatch import dispatcher
from ObjectListView import ObjectListView, ColumnDefn
import datetime
import csv
import os

class PingUnit(object):
    """
    Model of the Ping Unit
 
    Contains the following attributes:
    'hostname','serial','device','mac',
    """
    #----------------------------------------------------------------------
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
    #----------------------------------------------------------------------
    def __init__(self, ping_time, ms_delay, success):
        
        self.ping_time = ping_time
        self.ms_delay = ms_delay
        self.success = success
        
class DetailsView(wx.Dialog):
    
    def __init__(self, parent, device_object):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, 
                           pos=wx.DefaultPosition, size=wx.Size(400, 550), 
                           style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        
        bsizer1 = wx.BoxSizer(wx.VERTICAL)
        
        bsizer121 = wx.BoxSizer(wx.VERTICAL)
        
        self.ping_list = ObjectListView(self, wx.ID_ANY, size=wx.Size(-1, 500), 
                                        style=wx.LC_REPORT|
                                        wx.SUNKEN_BORDER|
                                        wx.RESIZE_BORDER)
        self.ping_list.SetColumns([ColumnDefn("Time", "center", 180, 
                           "ping_time", stringConverter="%d-%m-%Y %H:%M:%S.%f"),
                                   ColumnDefn("ms Delay", "center", 80,
                                                                    "ms_delay"),
                                   ColumnDefn("Success", "center", 80, 
                                                                     "success"),
                                   ])
        bsizer121.Add(self.ping_list, 1, wx.ALL|wx.EXPAND, 5)
        bsizer1.Add(bsizer121, 0, wx.EXPAND, 5)
        
               
        self.SetSizer(bsizer1)
        self.Layout()
        
        self.Centre(wx.BOTH)


        #------------------------------ Done with wxFormBuilder  
           
        self.parent = parent
        self.SetTitle("Details View for " + device_object.ip_address) 
        self.ping_list.SetObjects(device_object.ping_data)        
        
        
class MultiPing(wx.Dialog):
    
    def __init__(self, parent, device_list):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, 
                           pos=wx.DefaultPosition, size=wx.Size(710, 550), 
                           style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        
        bsizer1 = wx.BoxSizer(wx.VERTICAL)        
        bsizer121 = wx.BoxSizer(wx.VERTICAL)
        
        self.ping_list = ObjectListView(self, wx.ID_ANY, size=wx.Size(-1, 500), 
                                        style=wx.LC_REPORT|
                                        wx.SUNKEN_BORDER|
                                        wx.RESIZE_BORDER)
        self.ping_list.SetColumns([ColumnDefn("IP", "center", 100,
                                                                  "ip_address"),
                                   ColumnDefn("MAC", "center", 130, 
                                                                 "mac_address"),
                                   ColumnDefn("Hostname", "center", 130, 
                                                                    "hostname"),
                                   ColumnDefn("Serial", "center", 150, 
                                                                     "serial"),
                                   ColumnDefn("Successful Pings", "center", 80,
                                                                     "success"),
                                   ColumnDefn("Failed Pings", "center", 80, 
                                                                      "failed"),
                                   ])
        self.ping_list.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.on_right_click)  
        bsizer121.Add(self.ping_list, 1, wx.ALL|wx.EXPAND, 5)
        bsizer1.Add(bsizer121, 0, wx.EXPAND, 5)
        
               
        self.SetSizer(bsizer1)
        self.Layout()
        
        self.Centre(wx.BOTH)


        #------------------------------ Done with wxFormBuilder  
           
        self.parent = parent
        self.SetTitle("Multiple Ping Monitor")
        self.ping_objects = []
        self.set_objects(device_list)
        self.ping_list.SetObjects(self.ping_objects)
        self.log_files = {}

        for obj in device_list:
            self.parent.telnet_job_queue.put(['Ping', obj, 
                                            self.parent.telnet_timeout_seconds])
            
        for obj in self.ping_objects:
            self.log_files[obj]=('device_' + obj.ip_address + '_time_' + 
                                   datetime.datetime.now().strftime('%H_%M_%S') +
                                   '.csv')
        #print self.log_files  
            
        self.Bind(wx.EVT_CLOSE, self.on_close)
        dispatcher.connect(self.on_incoming_ping, 
                                signal="Incoming Ping", sender=dispatcher.Any)
        
        #print self.timer.IsRunning()
        
    #----------------------------------------------------------------------

 
    def on_redraw_timer(self, _):
        """Refresh objects when timer expires"""
        self.ping_list.RefreshObject(self.ping_objects)
 
    def set_objects(self, device_list):
        """Creates a ping object and adds it to the list"""
        for obj in device_list:
            
            data = [PingUnit(
                             [],
                             obj.hostname,
                             obj.serial,
                             obj.ip_address,
                             obj.mac_address
                            )]
            self.ping_objects.append(data[0])
            
    
    def set_ping_data(self, ping_info):
        """Makes a ping data unit"""
        data = [Ping_Data_Unit(
                               ping_info[0],  #.strftime('%H:%M:%S.%f')
                               ping_info[1],
                               ping_info[2],
                              )]
        return data[0]
        
    def on_incoming_ping(self, sender):
        """Process an incoming ping"""
        #switch to true to log pings
        logging = False
        #print sender
        #print '.'
        if self.parent.ping_active:
            #for item in sender:
            #print 'start incoming'
            #print sender[0]
            #print sender[0].ip
            for obj in self.ping_objects:

                
                if sender[0].ip_address == obj.ip_address:

                    obj.ping_data.append(self.set_ping_data(sender[1]))
              
                    if sender[1][2] == 'Yes':
                        obj.success += 1
                    else:
                        obj.failed += 1
                    #print 'success', str(obj.success)
                    #print 'finish incoming'
                    self.ping_list.RefreshObject(obj)
                    if logging:
                        self.save_log(obj)

        
    def on_close(self, _):
        """Close the window"""               
        self.parent.ping_active = False
        self.Hide()
        self.parent.ping_window = None
        self.Destroy()
        
        
    def show_details(self, _):
        """Show the details of the pings to this device"""        
        for obj in self.ping_list.GetSelectedObjects():
            dia = DetailsView(self, obj)
            dia.Show()
        
        
    def on_right_click(self, _):
        """Create a right click menu"""        
        right_click_menu = wx.Menu()                
        rcitem = right_click_menu.Append(wx.ID_ANY, 'Show Details', 
                                                                 'Show Details')
        self.Bind(wx.EVT_MENU, self.show_details, rcitem)  
        self.PopupMenu(right_click_menu)
        right_click_menu.Destroy()

    def save_log(self, obj):
        """Save log to a file"""
        user_path = os.path.expanduser('~\\Documents\\Magic_DXLink_Configurator\\')
        path = user_path + self.log_files[obj]
        
        with open(path, 'ab') as log_file:
            writer_csv = csv.writer(log_file, quoting=csv.QUOTE_ALL)
            row = []
            row.append(str(obj.ping_data[-1].ping_time))
            row.append(str(obj.ping_data[-1].ms_delay))
            row.append(str(obj.ping_data[-1].success))
            writer_csv.writerow(row)
            #print row
        

        



















































































