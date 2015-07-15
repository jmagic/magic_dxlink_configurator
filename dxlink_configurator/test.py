import requests
import os
import wx
import wx.lib.scrolledpanel as scrolled
 
from threading import Thread
from wx.lib.pubsub import pub
 
########################################################################
class DownloadThread(Thread):
    """Downloading thread"""
 
    #----------------------------------------------------------------------
    def __init__(self, gnum, url, fsize):
        """Constructor"""
        Thread.__init__(self)
        self.fsize = fsize
        self.gnum = gnum
        self.url = url
        self.start()
 
    #----------------------------------------------------------------------
    def run(self):
        """
        Run the worker thread
        """
        local_fname = os.path.basename(self.url)
        count = 1
        while True:
            if os.path.exists(local_fname):
                tmp, ext = os.path.splitext(local_fname)
                cnt = "(%s)" % count
                local_fname = tmp + cnt + ext
                count += 1
            else:
                break
        req = requests.get(self.url, stream=True)
        total_size = 0
        print local_fname
        with open(local_fname, "wb") as fh:
            for byte in req.iter_content(chunk_size=1024):
                if byte:
                    fh.write(byte)
                    fh.flush()
                total_size += len(byte)
                if total_size < self.fsize:
                    wx.CallAfter(pub.sendMessage, 
                                 "update_%s" % self.gnum,
                                 msg=total_size)
        print "DONE!"
        wx.CallAfter(pub.sendMessage,
                     "update_%s" % self.gnum,
                     msg=self.fsize)
 
 
########################################################################
class MyGauge(wx.Gauge):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent, range, num):
        """Constructor"""
        wx.Gauge.__init__(self, parent, range=range)
 
        pub.subscribe(self.updateProgress, "update_%s" % num)
 
    #----------------------------------------------------------------------
    def updateProgress(self, msg):
        """"""
        self.SetValue(msg)
 
########################################################################
class MyPanel(scrolled.ScrolledPanel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        scrolled.ScrolledPanel.__init__(self, parent)
 
        self.data = []
        self.download_number = 1
 
        # create the sizers
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        dl_sizer = wx.BoxSizer(wx.HORIZONTAL)
 
        # create the widgets
        lbl = wx.StaticText(self, label="Download URL:")
        self.dl_txt = wx.TextCtrl(self)
        btn = wx.Button(self, label="Download")
        btn.Bind(wx.EVT_BUTTON, self.onDownload)
 
        # layout the widgets
        dl_sizer.Add(lbl, 0, wx.ALL|wx.CENTER, 5)
        dl_sizer.Add(self.dl_txt, 1, wx.EXPAND|wx.ALL, 5)
        dl_sizer.Add(btn, 0, wx.ALL, 5)
        self.main_sizer.Add(dl_sizer, 0, wx.EXPAND)
 
        self.SetSizer(self.main_sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()
 
    #----------------------------------------------------------------------
    def onDownload(self, event):
        """
        Update display with downloading gauges
        """
        url = self.dl_txt.GetValue()
        try:
            header = requests.head(url)
            print header.is_redirect
            print header.url
            print dir(header)
            length = requests.
            fsize = int(header.headers["content-length"]) / 1024
 
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            fname = os.path.basename(url)
            lbl = wx.StaticText(self, label="Downloading %s" % fname)
            gauge = MyGauge(self, fsize, self.download_number)
 
            sizer.Add(lbl, 0, wx.ALL|wx.CENTER, 5)
            sizer.Add(gauge, 0, wx.ALL|wx.EXPAND, 5)
            self.main_sizer.Add(sizer, 0, wx.EXPAND)
 
            self.Layout()
 
            # start thread
            DownloadThread(self.download_number, url, fsize)
            self.dl_txt.SetValue("")
            self.download_number += 1
        except Exception, e:
            print "Error: ", e
 
########################################################################
class DownloaderFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Downloader", size=(800, 400))
        panel = MyPanel(self)
        self.Show()
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = DownloaderFrame()
    app.MainLoop()