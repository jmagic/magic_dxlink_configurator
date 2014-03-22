
import wx

from pydispatch import dispatcher

import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
import numpy as np
import pylab
import datetime
import csv
from ObjectListView import ObjectListView, ColumnDefn  

class PlotUnit(object):
    """
    Model of the Plot Unit
 
    Contains the following attributes:
    'hostname','serial','firmware','device','mac','time'
    """
    #----------------------------------------------------------------------
    def __init__(self, mse_data, ip, mac):
        
        self.mse_data = mse_data    
        self.ip = ip
        self.mac = mac
        
class MSE_Data_Unit(object):
    """
    Model of the MSE_Data_Unit

    Contains the following attributes:
    mse_time,mse_data0,mse_data1,mse_data2,mse_data3"""
    #----------------------------------------------------------------------
    def __init__(self, mse_time, mse_data0, mse_data1, mse_data2, mse_data3 ):
        
        self.mse_time = mse_time
        self.data0 = mse_data0
        self.data1 = mse_data1
        self.data2 = mse_data2
        self.data3 = mse_data3
        

class BoundControlBox(wx.Panel):

    def __init__(self, parent, ID, label, initval):
        wx.Panel.__init__(self, parent, ID)

        self.initval = initval
        direction = wx.VERTICAL if initval[3] else wx.HORIZONTAL
        
        sbSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, label ), direction )
        
        direction = wx.SL_HORIZONTAL if initval[3] else wx.SL_VERTICAL
         
        self.slider = wx.Slider( self, wx.ID_ANY, initval[0], initval[1], initval[2], wx.DefaultPosition, wx.Size(initval[4], -1), direction | wx.SL_LABELS | wx.SL_AUTOTICKS )
        self.slider.SetTickFreq(((abs(initval[1])+abs(initval[2]))/10),1)  #absolute value to deal with negitive numbers
        self.slider.Disable()
        sbSizer.Add( self.slider, 0, wx.ALL, 5 )

        self.radio_auto = wx.CheckBox( self, wx.ID_ANY, u"Auto", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.radio_auto.SetValue(True)
        sbSizer.Add( self.radio_auto, 0, wx.ALL, 5 )
        self.Bind(wx.EVT_CHECKBOX, self.on_checkbox, self.radio_auto )        
        
        self.SetSizer( sbSizer )
        self.Layout()
        sbSizer.Fit( self )
        
    def on_checkbox(self, event):
        if self.radio_auto.GetValue():
            self.slider.SetValue(self.initval[0])
            self.slider.Disable()
        else:
            self.slider.Enable()


class Multi_Plot ( wx.Dialog ):
    
    def __init__( self, parent, obj, plot_length ):
        
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 600,800 ), style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        self.panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
        self.bSizer10 = wx.BoxSizer( wx.VERTICAL )
        
        
        self.panel.SetSizer( self.bSizer10 )
        self.panel.Layout()
        self.bSizer10.Fit( self.panel )
        bSizer3.Add( self.panel, 1, wx.EXPAND |wx.ALL, 5 )

        bSizer1.Add( bSizer3, 0, wx.EXPAND, 5 )
        
        self.SetSizer( bSizer1 )

        device_list = [obj]

        self.parent = parent
        self.obj = obj
        self.SetTitle('MSE values plotted over time ' + obj.ip + '  ' + obj.device)
        self.plotObjects = []
        self.set_objects(device_list)
        self.paused = False
        self.threadNumber = ''
        self.plot_length = int(plot_length)
        
        self.error = [False, '']
        
        self.create_main_panel()

        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)        
        self.redraw_timer.Start((200+(100*(len(self.parent.mse_active_list))))) #slow refresh as multiple units are added

        dispatcher.connect(self.on_telnet_error, signal="MSE error", sender=dispatcher.Any)
        dispatcher.connect(self.on_incoming_mse, signal="Incoming MSE", sender=dispatcher.Any)
        

    def set_objects(self, device_list):
        for obj in device_list:
            data = [PlotUnit(
                             [],
                             obj.ip,
                             obj.mac
                             )]
            self.plotObjects.append(data[0])
            
    
    def set_mse_data(self, mse_info):
        data = [MSE_Data_Unit(
                               [mse_info[0].strftime('%H:%M:%S.%f')],
                               [int(mse_info[1][0])],
                               [int(mse_info[1][1])],
                               [int(mse_info[1][2])],
                               [int(mse_info[1][3])]
                               )]
        return(data[0])
                               

    def on_incoming_mse(self, sender):

        #print sender
        for obj in self.plotObjects:

            if not self.paused:
                if sender[2] == obj.mac:

                    if obj.mse_data == []:
                        obj.mse_data = self.set_mse_data(sender[0])
                    else:
                        obj.mse_data.mse_time.append(sender[0][0].strftime('%H:%M:%S.%f')) # an array of time
                        obj.mse_data.data0.append(int(sender[0][1][0])) #combine first data points into data0
                        obj.mse_data.data1.append(int(sender[0][1][1]))
                        obj.mse_data.data2.append(int(sender[0][1][2]))
                        obj.mse_data.data3.append(int(sender[0][1][3]))
                        
    '''def open_archive(self, archive):
        with open'''

    def on_telnet_error(self, sender):

        self.error = [True , sender]

    def create_main_panel(self):

        self.init_plot()
        
        self.canvas = FigCanvas(self.panel, -1, self.fig)
        
        self.length_control = BoundControlBox(self.panel, -1, "Length", [1500,150,1500,1,250]) # initval = [ default, min, max, direction 0=hoz 1=vert lenght of slider in px]
        self.time_control = BoundControlBox(self.panel, -1, "Time", [100,0,100,1,250])
        #self.time_control.slider.SetThumbLength(100)
        self.zoom_control = BoundControlBox(self.panel, -1, "Vertical zoom", [0,0,10,1,150])
        
        self.level_control = BoundControlBox(self.panel, -1, "Vertical level", [0,-17,15,1,150])
        
        self.pause_button = wx.Button(self.panel, -1, "Pause")
        self.Bind(wx.EVT_BUTTON, self.on_pause_button, self.pause_button)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_pause_button, self.pause_button)
        
        self.save_plot = wx.Button(self.panel, -1, "Save")
        self.Bind(wx.EVT_BUTTON, self.on_save_plot, self.save_plot)
        
        self.cb_xlab = wx.CheckBox(self.panel, -1, 
            "Show Labels as Time",
            style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.on_cb, self.cb_xlab)        
        self.cb_xlab.SetValue(True)
        
        self.cb_cha = wx.CheckBox(self.panel, -1, 
            "Show ChA",
            style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.on_cb, self.cb_cha)        
        self.cb_cha.SetValue(True)
        
        self.cb_chb = wx.CheckBox(self.panel, -1, 
            "Show ChB",
            style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.on_cb, self.cb_chb)        
        self.cb_chb.SetValue(True)
        
        self.cb_chc = wx.CheckBox(self.panel, -1, 
            "Show ChC",
            style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.on_cb, self.cb_chc)        
        self.cb_chc.SetValue(True)
        
        self.cb_chd = wx.CheckBox(self.panel, -1, 
            "Show ChD",
            style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.on_cb, self.cb_chd)        
        self.cb_chd.SetValue(True)
        
        #self.slider = wx.Slider(self.panel, -1, 750, 1, 1500,
        #    size=(250, -1),
        #    style= wx.ALIGN_RIGHT | wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS  )
        #self.slider.SetTickFreq(5,1)
        #self.Bind(wx.EVT_CHECKBOX, self.on_cb, self.slider)
        
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox1.Add(self.pause_button, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.Add(self.save_plot, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(20)
        self.hbox1.Add(self.cb_xlab, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(10)
        self.hbox1.Add(self.cb_cha, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(10)
        self.hbox1.Add(self.cb_chb, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(10)
        self.hbox1.Add(self.cb_chc, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(10)
        self.hbox1.Add(self.cb_chd, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        
        
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox2.Add(self.length_control, border=5, flag=wx.ALL)
        self.hbox2.Add(self.time_control, border=5, flag=wx.ALL)
        self.hbox2.Add(self.zoom_control, border=5, flag=wx.ALL)
        self.hbox2.Add(self.level_control, border=5, flag=wx.ALL)
        
        self.bSizer10.Add(self.canvas, -1, flag=wx.ALL|wx.EXPAND)
 
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas, 1, flag=wx.ALL|wx.EXPAND )        
        self.vbox.Add(self.hbox1, 0, flag=wx.ALIGN_LEFT | wx.TOP)
        self.vbox.Add(self.hbox2, 0, flag=wx.ALIGN_LEFT | wx.TOP)
        
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self) 
               
    
    def init_plot(self):
        self.dpi = 100
        self.fig = Figure((10.0, 3.5), dpi=self.dpi)
        self.fig.subplotpars.update(bottom = .20)
        self.axes = self.fig.add_subplot(111,  adjustable = 'box')
        self.axes.set_axis_bgcolor('black')

        pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes.get_yticklabels(), fontsize=8)
        
        
        # plot the data as a line series, and save the reference 
        # to the plotted line series
        #
        self.plot_data0 = self.axes.plot(
            [], 
            linewidth=1,
            color=("blue"),
            )[0]
        self.plot_data1 = self.axes.plot(
            [],
            linewidth=1,
            color=("red"),
            )[0]
        self.plot_data2 = self.axes.plot(
            [],
            linewidth=1,
            color=("green"),
            )[0]
        self.plot_data3 = self.axes.plot(
            [],
            linewidth=1,
            color=("white"),
            )[0]
            
        legend = self.fig.legend([self.plot_data0,self.plot_data1,self.plot_data2,self.plot_data3],['ChA','ChB','ChC','ChD'],'upper center',ncol=4,bbox_to_anchor=(0, 0, 1, 1), borderaxespad=0.)
        box = self.axes.get_position()
        self.axes.set_position([box.x0 - box.width * .11 , box.y0, box.width * 1.2, box.height])
        frame = legend.get_frame()
        frame.set_facecolor('0.90')
        for label in legend.get_texts():
            label.set_fontsize('small')

        for label in legend.get_lines():
            label.set_linewidth(1.5)

    def draw_plot(self):
        """ Redraws the plot
        """
        for obj in self.plotObjects:

            if obj.mse_data == []:
                break

            if self.length_control.radio_auto.IsChecked():
                
                end_point = self.length_control.slider.GetValue() if len(obj.mse_data.data0) < self.length_control.slider.GetValue() else len(obj.mse_data.data0)
                start_point = end_point - self.length_control.slider.GetValue()
            else:
                if len(obj.mse_data.data0) < self.length_control.slider.GetValue():
                    end_point =  self.length_control.slider.GetValue() 
                else:
                    end_point = ((self.time_control.slider.GetValue() * len(obj.mse_data.data0)) / 100) + self.length_control.slider.GetValue() 
                    if end_point > len(obj.mse_data.data0):
                        end_point = len(obj.mse_data.data0)  
            
                start_point = end_point - self.length_control.slider.GetValue()
            if not self.time_control.radio_auto.IsChecked():
            
                end_point = ((self.time_control.slider.GetValue() * len(obj.mse_data.data0)) / 100)
                start_point = end_point - self.length_control.slider.GetValue()
                if end_point < self.length_control.slider.GetValue():
                    end_point = self.length_control.slider.GetValue()
                    start_point = end_point - self.length_control.slider.GetValue()
            
            '''    #start_point = end_point - self.length_control.slider.GetValue()
                #if len(obj.mse_data.data0) < self.length_control.slider.GetValue():
                #    end_point = self.length_control.slider.GetValue()
                
                else:
                    end_point = ((self.time_control.slider.GetValue() * len(obj.mse_data.data0)) / 100)
                    if end_point < self.length_control.slider.GetValue():
                        end_point = self.length_control.slider.GetValue() 
            else:'''
                

            mse_time = obj.mse_data.mse_time[start_point:end_point]   #only get the number of plot points we will be ploting 
            data0 = obj.mse_data.data0[start_point:end_point] 
            data1 = obj.mse_data.data1[start_point:end_point] 
            data2 = obj.mse_data.data2[start_point:end_point] 
            data3 = obj.mse_data.data3[start_point:end_point] 

            
            xmin = 0 
            xmax = self.length_control.slider.GetValue()

            ymin = -4
            ymax = -25
            
            if not self.zoom_control.radio_auto.IsChecked():
                ymax = ymax + self.zoom_control.slider.GetValue() if self.level_control.radio_auto.IsChecked() else -25 + self.zoom_control.slider.GetValue() + self.level_control.slider.GetValue()
                ymin = ymin + (self.zoom_control.slider.GetValue()*-1) if self.level_control.radio_auto.IsChecked() else -4 + (self.zoom_control.slider.GetValue()*-1) + self.level_control.slider.GetValue()
                
            if not self.level_control.radio_auto.IsChecked():
                ymax = ymax  + self.level_control.slider.GetValue()
                ymin = ymin + self.level_control.slider.GetValue()
            
            self.axes.set_xbound(lower=xmin, upper=xmax)
            self.axes.set_ybound(lower=ymin, upper=ymax)
           
            self.axes.grid(True, color='gray')

            # Using setp here is convenient, because get_xticklabels
            # returns a list over which one needs to explicitly 
            # iterate, and setp already handles this.
            #  
            pylab.setp(self.axes.get_xticklabels(), 
               visible=True)

            if self.cb_cha.IsChecked():
                self.plot_data0.set_xdata(np.arange(len(data0)))
                self.plot_data0.set_ydata(np.array(data0))
            else:
                self.plot_data0.set_xdata([])
                self.plot_data0.set_ydata([])
                
            if self.cb_chb.IsChecked():
                self.plot_data1.set_xdata(np.arange(len(data1)))
                self.plot_data1.set_ydata(np.array(data1))
            else:
                self.plot_data1.set_xdata([])
                self.plot_data1.set_ydata([])  
                
            if self.cb_chc.IsChecked():
                self.plot_data2.set_xdata(np.arange(len(data2)))
                self.plot_data2.set_ydata(np.array(data2))
            else:
                self.plot_data2.set_xdata([])
                self.plot_data2.set_ydata([])
                
            if self.cb_chd.IsChecked():
                self.plot_data3.set_xdata(np.arange(len(data3)))
                self.plot_data3.set_ydata(np.array(data3))
            else:
                self.plot_data3.set_xdata([])
                self.plot_data3.set_ydata([])
           
            
            if self.cb_xlab.IsChecked():
                labels = []
                
                count = 0
                for item in self.axes.get_xticklabels():
    
                    count += 1
                    if len(self.axes.get_xticklabels()) == count:
                        break
                    item.set_rotation(35)
                    
                    try:
                        labels.append(mse_time[int(item.get_position()[0])][:-4])
                    except:
                        pass
            
    
                self.axes.set_xticklabels(labels)
            else:
                labels = []
                
                for item in self.axes.get_xticklabels():
                        item.set_rotation(35)
                        labels.append(int(item.get_position()[0]) + start_point)
                        
            
            self.axes.set_xticklabels(labels)    
        self.canvas.draw()
    
    def on_pause_button(self, event):
        self.paused = not self.paused

    
    def on_update_pause_button(self, event):
        label = "Resume" if self.paused else "Pause"
        self.pause_button.SetLabel(label)
    
    def on_cb(self, event):
        self.draw_plot()
    
    
    def on_save_plot(self, event):
        file_choices = "PNG (*.png)|*.png"
        name = 'device_' + self.obj.device + '_time_' + datetime.datetime.now().strftime('%H_%M_%S')
        dlg = wx.FileDialog(
            self, 
            message="Save plot as...",
            defaultDir=self.parent.path,
            defaultFile= name,
            wildcard=file_choices,
            style=wx.SAVE)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas.print_figure(path, dpi=self.dpi)
            datapath = dlg.GetPath()[:-4]
            datapath = datapath + ".csv"
            with open(datapath, 'wb') as f:
                w = csv.writer(f, quoting=csv.QUOTE_ALL)
                for obj in self.plotObjects:
                    w.writerow(['Time','ChA','ChB','ChC','ChD', self.obj.ip, self.obj.mac, self.obj.device])
                    for i in range(len(obj.mse_data.mse_time)):
                    
                        row = []
                        row.append(str(obj.mse_data.mse_time[i]))
                        row.append(str(obj.mse_data.data0[i]))
                        row.append(str(obj.mse_data.data1[i]))
                        row.append(str(obj.mse_data.data2[i]))
                        row.append(str(obj.mse_data.data3[i]))
                        w.writerow(row)
    
    def on_redraw_timer(self, sender):
        # if paused do not add data, but still redraw the plot
        # (to respond to scale modifications, grid change, etc.)
 
        if self.error[0] and self.obj.mac == self.error[1]:
            self.redraw_timer.Stop()
            dlg = wx.MessageDialog(parent=self, message= 'No connection to device ' + self.obj.ip, 
                                       caption = 'No %s' % self.obj.ip,
                                       style = wx.OK
                                       )
            dlg.ShowModal()
            dlg.Destroy()
            #self.on_close(None)
            self.error[0] = False
        #if not self.paused:
        self.draw_plot()
    
        
    def on_close(self, event):
        self.redraw_timer.Stop()
        self.parent.mse_active_list.remove(self.obj.mac)
        self.obj.mse_data = []
        self.Destroy()
        







