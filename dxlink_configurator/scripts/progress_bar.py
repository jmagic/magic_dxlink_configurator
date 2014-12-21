"""Progress bar for Magic DXLink Configurator"""

import wx
import csv
from scripts import mdc_gui


class Progress(mdc_gui.ProgressDialog):
    def __init__(self, parent):
        mdc_gui.ProgressDialog.__init__(self, parent)

        self.parent = parent
        self.set_values()
        dlg = wx.ProgressDialog(
            'Sending command to selected ' +
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

