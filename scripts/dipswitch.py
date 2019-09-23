"""For displaying the dipswitches"""

from . import mdc_gui


class ShowDipSwitch(mdc_gui.Dipswitch):
    def __init__(self, parent):
        mdc_gui.Dipswitch.__init__(self, parent)

        #set default values
        self.dip_one_slider.SetValue(0)
        self.dip_three_slider.SetValue(0)
        #set default lables
        self.on_switch_one(None)
        self.on_switch_two(None)
        self.on_switch_three(None)
        self.on_switch_four(None)


    def on_switch_one(self, _):
        """Toggle switch one"""
        if self.dip_one_slider.GetValue() > 0:
            self.dip_one_txt.SetLabel('#1 ISC/LAN port is DISABLED')
        else:
            self.dip_one_txt.SetLabel('#1 ISC/LAN port is ENABLED')
            

    def on_switch_two(self, _):
        """Toggle switch two"""
        if self.dip_two_slider.GetValue() > 0:
            self.dip_two_txt.SetLabel('#2 DXLink mode is MANUAL')
        else:
            self.dip_two_txt.SetLabel('#2 DXLink mode is AUTO')
            

    def on_switch_three(self, _):
        """Toggle switch three"""
        if self.dip_three_slider.GetValue() > 0:
            self.dip_three_txt.SetLabel('#3 Network connectivity is DISABLED')
        else:
            self.dip_three_txt.SetLabel('#3 Network connectivity is ENABLED')
            
    
    def on_switch_four(self, _):
        """Toggle switch four"""
        if self.dip_four_slider.GetValue() > 0:
            self.dip_four_txt.SetLabel('#4 Unidirectional mode is DISABLED') 
        else:
            self.dip_four_txt.SetLabel('#4 Unidirectional mode is ENABLED')
               
