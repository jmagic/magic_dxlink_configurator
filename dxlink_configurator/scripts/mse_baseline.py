"""Shows the baseline MSE values for a device"""
import wx
import wx.xrc
import wx.grid
from pydispatch import dispatcher
from collections import Counter

class PlotUnit(object):
    """
    Model of the Plot Unit
    Contains the following attributes:
    'hostname','serial','firmware','device','mac','time'
    """
    #----------------------------------------------------------------------
    def __init__(self, mse_data, ip_address, mac_address):

        self.mse_data = mse_data
        self.ip_address = ip_address
        self.mac_address = mac_address

class MSE_Data_Unit(object):
    """
    Model of the MSE_Data_Unit
    Contains the following attributes:
    mse_time,mse_data0,mse_data1,mse_data2,mse_data3"""
    #----------------------------------------------------------------------
    def __init__(self, mse_time, mse_data0, mse_data1, mse_data2, mse_data3):

        self.mse_time = mse_time
        self.data0 = mse_data0
        self.data1 = mse_data1
        self.data2 = mse_data2
        self.data3 = mse_data3


###########################################################################
## Class MSE Baseline Check
###########################################################################

class MSE_Baseline(wx.Dialog):
    
    def __init__(self, parent, obj):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, 
                            title=u"MSE Baseline Check", 
                            pos=wx.DefaultPosition, 
                            size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        
        bsizer1 = wx.BoxSizer(wx.VERTICAL)
        
        bsizer2 = wx.BoxSizer(wx.HORIZONTAL)

        bsizer3 = wx.BoxSizer(wx.VERTICAL)
        
        sbsizer3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, 
                                             u"Seconds elapsed"), wx.VERTICAL)
        
        self.m_statictext1 = wx.StaticText(self, wx.ID_ANY, 
                              u"0.0", wx.DefaultPosition, wx.Size(160, -1), 
                              wx.ALIGN_CENTRE)
        self.m_statictext1.Wrap(-1)
        self.m_statictext1.SetFont(wx.Font(48, 74, 90, 92, False, "Arial"))
        sbsizer3.Add(self.m_statictext1, 1, 
                    wx.ALL|
                    wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        bsizer3.Add(sbsizer3, 1, wx.EXPAND, 5)

        sbsizer4 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, 
                                            u"MSE Values taken"), wx.VERTICAL)
        
        self.m_statictext2 = wx.StaticText(self, wx.ID_ANY, 
                     u"0", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE)
        self.m_statictext2.Wrap(-1)
        self.m_statictext2.SetFont(wx.Font(48, 74, 90, 92, False, "Arial"))
        
        sbsizer4.Add(self.m_statictext2, 0, 
                                           wx.ALL|
                                           wx.ALIGN_LEFT, 5)
        
        
        bsizer3.Add(sbsizer4, 1, wx.EXPAND, 5)

        bsizer2.Add(bsizer3, 0, 0, 5)
        
        bsizer4 = wx.BoxSizer(wx.HORIZONTAL)
        
        sbsizer5 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, 
                                         u"Baseline MSE Values"), wx.VERTICAL)

        self.m_statictext14 = wx.StaticText(self, wx.ID_ANY, u"ChA = -00", 
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_statictext14.Wrap(-1)
        self.m_statictext14.SetFont(wx.Font(18, 74, 90, 90, False, "Arial"))
        
        sbsizer5.Add(self.m_statictext14, 0, wx.ALL, 5)
        
        self.m_statictext15 = wx.StaticText(self, wx.ID_ANY, u"ChB = -00",
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_statictext15.Wrap(-1)
        self.m_statictext15.SetFont(wx.Font(18, 74, 90, 90, False, "Arial"))
        
        sbsizer5.Add(self.m_statictext15, 0, wx.ALL, 5)
        
        self.m_statictext16 = wx.StaticText(self, wx.ID_ANY, u"ChC = -00", 
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_statictext16.Wrap(-1)
        self.m_statictext16.SetFont(wx.Font(18, 74, 90, 90, False, "Arial"))
        
        sbsizer5.Add(self.m_statictext16, 0, wx.ALL, 5)
        
        self.m_statictext17 = wx.StaticText(self, wx.ID_ANY, u"ChD = -00", 
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_statictext17.Wrap(-1)
        self.m_statictext17.SetFont(wx.Font(18, 74, 90, 90, False, "Arial"))
        
        sbsizer5.Add(self.m_statictext17, 0, wx.ALL, 5)
        
        
        bsizer4.Add(sbsizer5, 0, wx.ALIGN_CENTER_VERTICAL| wx.EXPAND, 5)
        
         
        bsizer2.Add(bsizer4, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        
        bsizer5 = wx.BoxSizer(wx.VERTICAL)
        
        sbsizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, 
                                                     u"MSE Table"), wx.VERTICAL)
        
        self.m_grid1 = wx.grid.Grid(self, wx.ID_ANY, wx.DefaultPosition, 
                                                              wx.DefaultSize, 0)
        
        # Grid
        self.m_grid1.CreateGrid(7, 2)
        self.m_grid1.EnableEditing(False)
        self.m_grid1.EnableGridLines(True)
        self.m_grid1.EnableDragGridSize(False)
        self.m_grid1.SetMargins(0, 0)
        
        # Columns
        self.m_grid1.SetColSize(0, 120)
        self.m_grid1.SetColSize(1, 160)
        self.m_grid1.EnableDragColMove(False)
        self.m_grid1.EnableDragColSize(False)
        self.m_grid1.SetColLabelSize(30)
        self.m_grid1.SetColLabelValue(0, u"MSE Value")
        self.m_grid1.SetColLabelValue(1, u"Cable Quality")
        self.m_grid1.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        
        # Rows
        self.m_grid1.AutoSizeRows()
        self.m_grid1.EnableDragRowSize(False)
        self.m_grid1.SetRowLabelSize(0)
        self.m_grid1.SetRowLabelValue(0, wx.EmptyString)
        self.m_grid1.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        
        # Label Appearance
        
        # Cell Defaults
        self.m_grid1.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)

        #self.m_grid.SetCellValue(row, col,"cell (%d,%d)" % (row, col))
        cell_text = [('Unlinked', 'No cable connected'),
                     ('0dB to -8dB', 'Unusable -- Likely no link made'),
                     ('-9dB to -11dB', 'Bad -- Likely no video'),
                     ('-12dB to -14dB', 'Poor -- Frequent video drops'), 
                     ('-15dB to -17dB', 'OK -- Rare video drops'),
                     ('-18dB to -20dB', 'Good -- Stable'),
                     ('-21dB to -23dB', 'Ideal -- Very robust')]
        for idx, item in enumerate(cell_text):
            self.m_grid1.SetCellValue(idx, 0, item[0])
            self.m_grid1.SetCellValue(idx, 1, item[1])



        sbsizer1.Add(self.m_grid1, 0, wx.ALL, 5)
        
        bsizer5.Add(sbsizer1, 1, wx.EXPAND, 5)

        bsizer2.Add(bsizer5, 1, wx.EXPAND, 5)
               
        bsizer1.Add(bsizer2, 1, wx.EXPAND, 5)
    
        m_sdbsizer1 = wx.StdDialogButtonSizer()
        #self.m_sdbsizer1save = wx.Button(self, wx.ID_SAVE)
        #m_sdbsizer1.AddButton(self.m_sdbsizer1save)
        self.m_sdbsizer1cancel = wx.Button(self, wx.ID_CANCEL)
        m_sdbsizer1.AddButton(self.m_sdbsizer1cancel)
        m_sdbsizer1.Realize()
        
        bsizer1.Add(m_sdbsizer1, 0, wx.ALIGN_RIGHT|wx.EXPAND|wx.ALL, 5)
        
        self.SetSizer(bsizer1)
        self.Layout()
        bsizer1.Fit(self)
        
        self.Centre(wx.BOTH)
        
        self.parent = parent
        self.obj = obj
        if self.obj.ip_address[:3] == "COM":
            self.SetTitle('MSE Baseline ' + 
                       'DGX ' + obj.mac_address)
        else:
            self.SetTitle('MSE Baseline ' + 
                       obj.ip_address + '  ' + obj.device)
        self.plot_obj = PlotUnit(
                                     [],
                                     obj.ip_address,
                                     obj.mac_address
                                     )

        #self.plot_length = int(plot_length)
        self.error = [False, '']
        self.ten_seconds = 0
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_BUTTON, self.on_close, self.m_sdbsizer1cancel)
        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)
        self.redraw_timer.Start((100))
        dispatcher.connect(self.on_telnet_error, signal="MSE error", 
                                                          sender=dispatcher.Any)
        dispatcher.connect(self.on_incoming_mse, signal="Incoming MSE", 
                                                          sender=dispatcher.Any)

    def set_mse_data(self, mse_info):
        """Creates data units"""
        data = MSE_Data_Unit(
                               [mse_info[0].strftime('%H:%M:%S.%f')],
                               [int(mse_info[1][0])],
                               [int(mse_info[1][1])],
                               [int(mse_info[1][2])],
                               [int(mse_info[1][3])]
                               )
        return data

    def on_incoming_mse(self, sender):
        """Handle incoming MSE values"""
        if sender[2] == self.plot_obj.mac_address:

            if self.plot_obj.mse_data == []:
                self.plot_obj.mse_data = self.set_mse_data(sender[0])
            else:
                self.plot_obj.mse_data.mse_time.append(
                                   sender[0][0].strftime('%H:%M:%S.%f')) 
                self.plot_obj.mse_data.data0.append(int(sender[0][1][0])) 
                self.plot_obj.mse_data.data1.append(int(sender[0][1][1]))
                self.plot_obj.mse_data.data2.append(int(sender[0][1][2]))
                self.plot_obj.mse_data.data3.append(int(sender[0][1][3]))

    def on_telnet_error(self, sender):
        """Handle telnet error"""
        self.error = [True, sender]

    def on_redraw_timer(self, _):
        """Update plot when timer expires"""
        if self.error[0] and self.plot_obj.mac_address == self.error[1]:
            self.redraw_timer.Stop()
            dlg = wx.MessageDialog(parent=self, 
                      message='No connection to device ' + 
                      self.plot_obj.ip_address,
                      caption='No %s' % self.plot_obj.ip_address,
                      style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            self.error[0] = False

        if self.plot_obj.mse_data == []:
            pass
        else:
            self.ten_seconds = self.ten_seconds + .1
            self.m_statictext1.SetLabel(str(int(self.ten_seconds)))

            self.m_statictext2.SetLabel(str(len(self.plot_obj.mse_data.data0)))
            
            cha_common = Counter(self.plot_obj.mse_data.data0).most_common(1)[0][0]
            chb_common = Counter(self.plot_obj.mse_data.data1).most_common(1)[0][0]
            chc_common = Counter(self.plot_obj.mse_data.data2).most_common(1)[0][0]
            chd_common = Counter(self.plot_obj.mse_data.data3).most_common(1)[0][0]

            self.m_statictext14.SetLabel('ChA = ' + 
                                          str(cha_common))
            new_color = self.set_color(cha_common)
            self.m_statictext14.SetForegroundColour(wx.Colour(new_color[0],
                                                              new_color[1],
                                                              new_color[2])) 
            self.m_statictext15.SetLabel('ChB = ' + 
                                          str(chb_common))
            new_color = self.set_color(chb_common)
            self.m_statictext15.SetForegroundColour(wx.Colour(new_color[0],
                                                              new_color[1],
                                                              new_color[2])) 
            self.m_statictext16.SetLabel('ChC = ' + 
                                          str(chc_common))
            new_color = self.set_color(chc_common)
            self.m_statictext16.SetForegroundColour(wx.Colour(new_color[0],
                                                              new_color[1],
                                                              new_color[2])) 
            self.m_statictext17.SetLabel('ChD = ' + 
                                          str(chd_common))
            new_color = self.set_color(chd_common)
            self.m_statictext17.SetForegroundColour(wx.Colour(new_color[0],
                                                              new_color[1],
                                                              new_color[2])) 


            #print self.ten_seconds
            #print type(self.ten_seconds)
            if self.ten_seconds >= 10:
                self.on_complete()

    def set_color(self, mse_value):
        """Set the color of the mse"""
        mse_color = (0, 0, 0)
        if 0 >= mse_value >= -14:
            mse_color = (255, 0, 0)
        if -15 >= mse_value >= -17:
            mse_color = (255, 255, 128)
        if -18 >= mse_value >= -23:
            mse_color = (0, 255, 0)
        return mse_color


    def on_complete(self):
        """Stop taking mse values"""
        self.redraw_timer.Stop()
        #print self.plot_obj.mse_data.data0

    def on_close(self, _):
        """User closes the plot window"""
        self.redraw_timer.Stop()
        self.parent.mse_active_list.remove(self.obj.mac_address)
        if self.obj.ip_address[:3] == "COM":
            self.parent.serial_active.remove(self.obj.mac_address)
        self.plot_obj.mse_data = []
        self.Destroy()

    def __del__(self):
        pass
