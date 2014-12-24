
class Prog:
    def __init__(self):
        self.name = None

    def start(self, func, *args): # helper method to run a function in another thread
        thread = threading.Thread(target=func, args=args)
        thread.setDaemon(True)
        thread.start()


    def display_progress(self):
        """Shows progress of connections"""
        if len(self.main_list.GetSelectedObjects()) == 1:
            dialog = wx.ProgressDialog(
                'Attempting connect to selected device',
                'Attempting connection to selected device')
        else:
            dialog = wx.ProgressDialog(
                'Attempting connect to selected devices',
                'Attempting connection to all selected devices',
                maximum=len(self.main_list.GetSelectedObjects()))

        self.start(self.progress_processing, dialog)
        dialog.ShowModal()

    def progress_processing(self, dialog):
        """Set up progress dialog"""
        if len(self.main_list.GetSelectedObjects()) == 1:
            wx.CallAfter(dialog.Pulse)

            while ((len(self.completionlist) + len(self.errorlist)) <
                   len(self.main_list.GetSelectedObjects())):
                count = (len(self.completionlist) + len(self.errorlist))
                time.sleep(.01)
                wx.CallAfter(dialog.Pulse)
        else:
            while ((len(self.completionlist) + len(self.errorlist)) <
                   len(self.main_list.GetSelectedObjects())):
                count = (len(self.completionlist) + len(self.errorlist))
                wx.CallAfter(
                    dialog.Update, 
                    count, 
                    "Attempting connection to %s of %s devices" % (
                        (count + 1), 
                        len(self.main_list.GetSelectedObjects())))

        dialog.Destroy()

        errortext = ""
        for i in range(len(self.errorlist)):
            errortext = (
                errortext + 
                self.errorlist[i][0].ip_address + "    " + 
                self.errorlist[i][1] + "\n")

        completiontext = ""
        for i in range(len(self.completionlist)):
            completiontext = (
                completiontext + 
                self.completionlist[i].ip_address + "     " +
                self.completionlist[i].model + "\n")
        
        if len(self.errorlist) == len(self.main_list.GetSelectedObjects()):
            dlg = wx.MessageDialog(
                parent=self,
                message='Failed to connect to \n=======================' + 
                ' \n%s ' % errortext,
                caption='Failed connection list',
                style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        elif len(self.completionlist) == \
             len(self.main_list.GetSelectedObjects()):
            if self.displaysuccess:
                dlg = wx.MessageDialog(
                    parent=self,
                    message='Successfully connected to: \n' +
                    '=======================\n%s' % completiontext,
                    caption='Connection list',
                    style=wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
        else:
            dlg = wx.MessageDialog(
                parent=self, 
                message='Failed to connect to: \n======================= ' +
                '\n%s \n \n' % (errortext) +
                'Successfully connected to: \n=======================' +
                ' \n%s' % (completiontext),
                caption='Connection list',
                style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        self.main_list.RefreshObjects(self.main_list.GetObjects())
        self.dump_pickle()
        self.errorlist = []
        self.completionlist = []