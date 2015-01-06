"""For displaying the dipswitches"""

import mdc_gui


class ShowDipSwitch(mdc_gui.Dipswitch):
    def __init__(self, parent, device_object):
        mdc_gui.Dipswitch.__init__(self, parent)

        self.obj = device_object
        self.dip_one_slider.Disable()
        self.dip_two_slider.Disable()
        self.dip_three_slider.Disable()
        self.dip_four_slider.Disable()

        