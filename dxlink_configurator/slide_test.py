import wx
import wx.grid as gridlib
import datetime

class MainPanel(wx.Panel):

    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent, style=wx.BORDER_SUNKEN)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.smBtn = wx.Button(self, -1, "Show Bar")
        self.dmBtn = wx.Button(self, -1, "Hide Bar")

        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.button_sizer.Add(self.smBtn, 0)
        self.button_sizer.Add(self.dmBtn, 0)

        self.Bind(wx.EVT_BUTTON, self.OnShowMessage, self.smBtn)
        self.Bind(wx.EVT_BUTTON, self.OnDismiss, self.dmBtn)


        self.side_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.side_grid = SideGrid(self)
        self.side_grid.Show(False)
        self.testBtn = wx.Button(self, -1, "test button")


        self.side_sizer.Add(self.testBtn, 0)
        self.side_sizer.Add(self.side_grid, 1, wx.EXPAND)

        self.mainSizer.Add(self.button_sizer, 0)
        self.mainSizer.Add(self.side_sizer, 1, wx.EXPAND)

        self.SetSizer(self.mainSizer)

    def OnShowMessage(self, evt):
        self.testBtn.Hide()
        #self.side_sizer.Detach(self.testBtn)
        #self.test
        self.side_grid.ShowMessage("abc")

        self.side_grid.Refresh()
        self.side_sizer.Layout()
        #self.mainSizer.Layout()

        self.Refresh()


    def OnDismiss(self, evt):
        self.side_grid.Dismiss()
        #self.side_sizer.Add(self.testBtn, 1)
        self.testBtn.Show(True)


class SideGrid(wx.InfoBar):
    def __init__(self, parent, *args, **kwargs):

        wx.InfoBar.__init__(self, parent)

        self.my_grid = gridlib.Grid(self, -1, name="My Grid")
        self.SetShowHideEffects(wx.SHOW_EFFECT_SLIDE_TO_LEFT, wx.SHOW_EFFECT_SLIDE_TO_RIGHT)

        self.num_of_rows = 12*10
        self.my_grid.CreateGrid(self.num_of_rows, 3)
        self.my_grid.SetDefaultCellAlignment(wx. ALIGN_CENTRE , wx. ALIGN_CENTRE )
        self.my_grid.HideRowLabels()
        self.my_grid.SetColLabelValue(0, "COLA")
        self.my_grid.SetColLabelValue(1, "COLB")
        self.my_grid.SetColLabelValue(2, "COLC")

        current = datetime.datetime(2014,8,1)
        for month_ix in xrange(self.num_of_rows):
            new_month = current.month%12 + 1
            new_year = current.year + current.month // 12
            current = current.replace(month=new_month, year=new_year)
            self.my_grid.SetCellValue(month_ix, 0, current.strftime("%Y %b"))

        for row in xrange(0,12*10):
            for col in xrange(1,3):
                self.my_grid.SetCellValue(row, col, "80")

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.my_grid, 1, wx.EXPAND)
        self.SetSizerAndFit(self.sizer)

class MyForm(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Sliding grid")
        self.main_panel = MainPanel(self)

if __name__ == "__main__":
    app = wx.App(False)
    #mport wx.lib.inspection
    #wx.lib.inspection.InspectionTool().Show()
    frame = MyForm()
    frame.Show()
    app.MainLoop()