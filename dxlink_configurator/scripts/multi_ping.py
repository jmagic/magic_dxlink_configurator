import wx
from pydispatch import dispatcher

from ObjectListView import ObjectListView, ColumnDefn
import time


class PingUnit(object):
    """
    Model of the Ping Unit
 
    Contains the following attributes:
    'hostname','serial','device','mac',
    """
    #----------------------------------------------------------------------
    def __init__(self, ping_data, hostname, serial, ip, mac):
        
        self.ping_data = ping_data    
        self.hostname = hostname
        self.serial = serial
        self.ip = ip
        self.mac = mac
        self.success = 0
        self.failed = 0

        
class Ping_Data_Unit(object):
    """
    Model of the Ping_Data_Unit

    Contains the following attributes:
    ping_time, ms delay, successful """
    #----------------------------------------------------------------------
    def __init__(self, ping_time, ms_delay, success ):
        
        self.ping_time = ping_time
        self.ms_delay = ms_delay
        self.success = success
        

    

        
class DetailsView ( wx.Dialog ):
    
    def __init__( self, parent, device_object ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 400,550 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer121 = wx.BoxSizer( wx.VERTICAL )
        
        self.deviceOlv = ObjectListView(self, wx.ID_ANY, size = wx.Size( -1,500), style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.RESIZE_BORDER )
        self.deviceOlv.SetColumns([ColumnDefn("Time", "center", 180, "ping_time", stringConverter="%d-%m-%Y %H:%M:%S.%f"),
                                   ColumnDefn("ms Delay", "center", 80, "ms_delay"),
                                   ColumnDefn("Success", "center", 80, "success"),
                                   ])
        bSizer121.Add( self.deviceOlv, 1, wx.ALL|wx.EXPAND, 5 )
        bSizer1.Add ( bSizer121, 0, wx.EXPAND, 5)
        
               
        self.SetSizer( bSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )


        #------------------------------ Done with wxFormBuilder  
           
        self.parent = parent
        self.SetTitle("Details View for " + device_object.ip)
        viewObjects = []
        #print dir(device_object.ping_data[0])
        
        
        '''x = 0
        for obj in device_object.ping_data.ping_time:
            print obj
            print device_object.ms_delay[x]
            print device_object.success[x]
            #viewObjects.append(obj)
        '''    
        
            
        self.deviceOlv.SetObjects(device_object.ping_data)
        
            
        #self.Bind(wx.EVT_CLOSE, self.on_close)
        
       
        
        
        
class MultiPing ( wx.Dialog ):
    
    def __init__( self, parent, device_list ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 710,550 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer121 = wx.BoxSizer( wx.VERTICAL )
        
        self.deviceOlv = ObjectListView(self, wx.ID_ANY, size = wx.Size( -1,500), style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.RESIZE_BORDER )
        self.deviceOlv.SetColumns([ColumnDefn("IP", "center", 100, "ip"),
                                   ColumnDefn("MAC", "center", 130, "mac"),
                                   ColumnDefn("Hostname", "center", 130, "hostname"),
                                   ColumnDefn("Serial", "center", 150, "serial"),
                                   ColumnDefn("Successful Pings", "center", 80, "success"),
                                   ColumnDefn("Failed Pings", "center", 80, "failed"),
                                   ])
        self.deviceOlv.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)  # right click menu
        bSizer121.Add( self.deviceOlv, 1, wx.ALL|wx.EXPAND, 5 )
        bSizer1.Add ( bSizer121, 0, wx.EXPAND, 5)
        
               
        self.SetSizer( bSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )


        #------------------------------ Done with wxFormBuilder  
           
        self.parent = parent
        self.SetTitle("Multiple Ping Monitor")
        self.pingObjects = []
        self.set_objects(device_list)
        
        #self.deviceOlv.SetColumns([ColumnDefn("Model", "center", 130, "model"),ColumnDefn("IP", "center", 100, "ip"),ColumnDefn("Device", "center", 80, "device")])
        #self.deviceOlv.CreateCheckStateColumn()
        self.deviceOlv.SetObjects(self.pingObjects)
        #objects = self.deviceOlv.GetObjects()
        #self.default_obj = objects[0]
        #for obj in objects:
        #   #self.default_obj = obj
        #    self.deviceOlv.ToggleCheck(obj)
        #    self.set_pinging(obj)
            
        #self.deviceOlv.RefreshObjects(objects)
        for obj in device_list:
            self.parent.telnetjobqueue.put(['Ping', obj, self.parent.telnet_timeout_seconds])   
            
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
        #self.redraw_timer = wx.Timer(self)
        #self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)        
        #self.redraw_timer.Start((1000))
        
        #self.parent.jobqueue.put(['Ping', None , self.parent.telnet_timeout_seconds])
        dispatcher.connect(self.on_incoming_ping, signal="Incoming Ping", sender = dispatcher.Any)
        
        #print self.timer.IsRunning()
        
    #----------------------------------------------------------------------

 
    def on_redraw_timer(self, data=None):
        #print 'refresh'
        self.deviceOlv.RefreshObjects(self.pingObjects)
 
    def set_objects(self, device_list):
        for obj in device_list:
            
            data = [PingUnit(
                             [],
                             obj.hostname,
                             obj.serial,
                             obj.ip,
                             obj.mac
                             )]
            self.pingObjects.append(data[0])
            
    
    def set_ping_data(self, ping_info):
        data = [Ping_Data_Unit(
                               ping_info[0],  #.strftime('%H:%M:%S.%f')
                               ping_info[1],
                               ping_info[2],
                               )]
        return(data[0])
        
    def on_incoming_ping(self, sender):

        #print sender
        #print '.'
        if self.parent.ping_active:
            #for item in sender:
            #print 'start incoming'
            #print sender[0]
            #print sender[0].ip
            for obj in self.pingObjects:

                
                if sender[0].ip == obj.ip:

                    obj.ping_data.append(self.set_ping_data(sender[1]))
                    '''
                    else:
                         obj.ping_data.ping_time.append(sender[1][0]) #.strftime('%H:%M:%S.%f')) # an array of time
                        obj.ping_data.ms_delay.append(sender[1][1])
                        obj.ping_data.success.append(sender[1][2])
                    #print str(obj.ping_data.ms_delay)
                    #print "obj.ping_data.success", str(obj.ping_data.success)
                    '''
               
                    if sender[1][2] == 'Yes':
                        obj.success += 1
                    else:
                        obj.failed += 1
                    #print 'success', str(obj.success)
                    #print 'finish incoming'
                    self.deviceOlv.RefreshObject(obj)
        else:
            pass

    def onTimeOut(self, event):
        #self.deviceOlv.RefreshObjects()
        pass
        
    def on_close(self, event):
        
        
        self.parent.ping_active = False
        #self.redraw_timer.Stop()
        self.Hide()
        self.Destroy()
        
    def showDetails(self, event):
        
        for obj in self.deviceOlv.GetSelectedObjects():
            dia = DetailsView(self, obj)
            dia.Show()
        
        
    def onRightClick(self, event):
        
        right_click_Menu = wx.Menu()
                
        rcitem = right_click_Menu.Append(wx.ID_ANY, 'Show Details', 'Show Details')
        self.Bind(wx.EVT_MENU, self.showDetails, rcitem)  
        
        self.PopupMenu(right_click_Menu)
        right_click_Menu.Destroy()

     
        































































































