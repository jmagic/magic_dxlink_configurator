import wx
from scripts import mdc_gui
from pydispatch import dispatcher
from dataclasses import dataclass, field
from collections import Counter


@dataclass
class PlotUnit:
    """A MSE Value"""
    mse_data: list = field(default_factory=list)
    obj: object = None


@dataclass
class MSEDataUnit:
    mse_time: str = ""
    data0: list = field(default_factory=list)
    data1: list = field(default_factory=list)
    data2: list = field(default_factory=list)
    data3: list = field(default_factory=list)


class MSEBaseline(mdc_gui.MSE_Baseline):
    def __init__(self, parent, obj):
        mdc_gui.MSE_Baseline.__init__(self, parent)
        cell_text = [('Unlinked', ' ', 'No cable connected'),
                     ('0dB to -8dB', ' ', 'Unusable -- Likely no link made'),
                     ('-9dB to -11dB', ' ', 'Bad -- Likely no video'),
                     ('-12dB to -14dB', ' ', 'Poor -- Frequent video drops'),
                     ('-15dB to -17dB', ' ', 'OK -- Rare video drops'),
                     ('-18dB to -20dB', ' ', 'Good -- Stable'),
                     ('-21dB to -23dB', ' ', 'Ideal -- Very robust')]
        for idx, item in enumerate(cell_text):
            self.mse_manual_grid.SetCellValue(idx, 0, item[0])
            self.mse_manual_grid.SetCellValue(idx, 1, item[1])
            self.mse_manual_grid.SetCellValue(idx, 2, item[2])
        for i in range(4):
            self.mse_manual_grid.SetCellBackgroundColour(i, 1, (255, 0, 0))
        self.mse_manual_grid.SetCellBackgroundColour(4, 1, (255, 128, 64))
        for i in range(5, 7):
            self.mse_manual_grid.SetCellBackgroundColour(i, 1, (0, 255, 0))
        self.mse_manual_grid.AutoSize()

        self.Layout()
        self.parent = parent
        self.obj = obj
        if self.obj.ip_address[:3] == "COM":
            self.SetTitle(f'MSE Baseline DGX {obj.mac_address}')
        else:
            self.SetTitle(f'MSE Baseline {obj.ip_address} {obj.device}')
        self.plot_obj = PlotUnit([], obj)

        # self.plot_length = int(plot_length)
        self.error = [False, '']
        self.complete = False
        self.ten_seconds = 0
        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)
        self.redraw_timer.Start((100))
        dispatcher.connect(self.on_telnet_error, signal="MSE error", sender=dispatcher.Any)
        dispatcher.connect(self.on_incoming_mse, signal="Incoming MSE", sender=dispatcher.Any)

    def set_mse_data(self, mse_info):
        """Creates data units"""
        data = MSEDataUnit([mse_info.report_time.strftime('%H:%M:%S.%f')],
                           [mse_info.mse[0]],
                           [mse_info.mse[1]],
                           [mse_info.mse[2]],
                           [mse_info.mse[3]])
        return data

    def on_incoming_mse(self, sender, data):
        """Handle incoming MSE values"""
        if data.obj == self.plot_obj.obj:

            if self.plot_obj.mse_data == []:
                self.plot_obj.mse_data = self.set_mse_data(data)
            else:
                self.plot_obj.mse_data.mse_time.append(data.report_time.strftime('%H:%M:%S.%f'))
                self.plot_obj.mse_data.data0.append(data.mse[0])
                self.plot_obj.mse_data.data1.append(data.mse[1])
                self.plot_obj.mse_data.data2.append(data.mse[2])
                self.plot_obj.mse_data.data3.append(data.mse[3])
        # print(self.plot_obj)

    def on_telnet_error(self, sender):
        """Handle telnet error"""
        self.error = [True, sender]

    def on_redraw_timer(self, _):
        """Update plot when timer expires"""
        if self.error[0] and self.plot_obj.obj.mac_address == self.error[1]:
            self.redraw_timer.Stop()
            dlg = wx.MessageDialog(parent=self,
                                   message=f'No connection to device {self.plot_obj.obj.ip_address}',
                                   caption=f'No {self.plot_obj.obj.ip_address}',
                                   style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            self.error[0] = False

        if self.plot_obj.mse_data == []:
            pass
        else:
            self.ten_seconds = self.ten_seconds + .1
            # take all the values we have so far and find the most common
            cha_common = Counter(self.plot_obj.mse_data.data0).most_common(1)[0][0]
            chb_common = Counter(self.plot_obj.mse_data.data1).most_common(1)[0][0]
            chc_common = Counter(self.plot_obj.mse_data.data2).most_common(1)[0][0]
            chd_common = Counter(self.plot_obj.mse_data.data3).most_common(1)[0][0]

            # sometimes unlinked MSE will show -255
            # just set these to 0 to elminate confusion
            if cha_common == -255:
                cha_common = 0
            if chb_common == -255:
                chb_common = 0
            if chc_common == -255:
                chc_common = 0
            if chd_common == -255:
                chd_common = 0

            self.cha_txt.SetLabel('ChA = ' + str(cha_common))
            new_color = self.set_color(cha_common)
            self.cha_txt.SetForegroundColour(wx.Colour(*new_color))
            self.chb_txt.SetLabel('ChB = ' + str(chb_common))
            new_color = self.set_color(chb_common)
            self.chb_txt.SetForegroundColour(wx.Colour(*new_color))
            self.chc_txt.SetLabel('ChC = ' + str(chc_common))
            new_color = self.set_color(chc_common)
            self.chc_txt.SetForegroundColour(wx.Colour(*new_color))
            self.chd_txt.SetLabel('ChD = ' + str(chd_common))
            new_color = self.set_color(chd_common)
            self.chd_txt.SetForegroundColour(wx.Colour(*new_color))

            # print self.ten_seconds
            # print type(self.ten_seconds)
            if self.ten_seconds >= 10:
                self.on_complete()

    def set_color(self, mse_value):
        """Set the color of the mse"""
        mse_color = (0, 0, 0)
        if 0 >= mse_value >= -14:
            mse_color = (255, 0, 0)
        if -15 >= mse_value >= -17:
            mse_color = (255, 128, 64)
        # (255, 255, 128)
        if -18 >= mse_value >= -23:
            mse_color = (0, 255, 0)
        return mse_color

    def on_complete(self):
        """Stop taking mse values"""
        self.redraw_timer.Stop()
        self.parent.mse_active_list.remove(self.obj.mac_address)
        if self.obj.ip_address[:3] == "COM":
            self.parent.serial_active.remove(self.obj.mac_address)
        self.complete = True

    def on_close(self, _):
        """User closes the plot window"""
        self.redraw_timer.Stop()
        if not self.complete:
            self.parent.mse_active_list.remove(self.obj.mac_address)
            if self.obj.ip_address[:3] == "COM":
                self.parent.serial_active.remove(self.obj.mac_address)
        self.plot_obj.mse_data = []
        self.Destroy()
