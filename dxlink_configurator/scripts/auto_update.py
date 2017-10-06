import os
import sys
import wx
from requests import get as r_get
from distutils.version import StrictVersion
from threading import Thread


class AutoUpdate(Thread):
    def __init__(self, parent, version, name):
        Thread.__init__(self)
        self.parent = parent
        self.version = version
        self.server_name = 'http://magicsoftware.ornear.com'
        self.name = name
        self.short_name = ''   # just the initals
        self.path_name = ''    # lower with _
        self.common_name = ''  # Captilized name with _
        for item in self.name.split():
            self.short_name += item[:1].lower()
            self.path_name += item.lower() + '_'
            self.common_name += item + '_'
        self.path_name = self.path_name[:-1]
        self.common_name = self.common_name[:-1]

    def resource_path(self, relative):
        return os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(".")),
                            relative)

    def run(self):
        """Checks on line for updates"""
        try:
            update_url = (self.server_name +
                          '/current_version/' +
                          self.short_name +
                          '_current_version.txt')
            webpage = r_get(update_url)
            online_version = webpage.text[1:]
            if StrictVersion(online_version) > StrictVersion(self.version[1:]):
                self.do_update(update_url, online_version)
            else:
                return
        except Exception as error:
            print("Error in update_check: ", error)

    def do_update(self, url_path, online_version):
        """download and install"""
        # ask if they want to update
        dlg = wx.MessageDialog(parent=self.parent,
                               message=self.name + ' v' +
                               str(StrictVersion(online_version)) +
                               ' is available. \r' +
                               'Do you want to download and update?',
                               caption='Do you want to update?',
                               style=wx.OK | wx.CANCEL)
        if dlg.ShowModal() != wx.ID_OK:
            dlg.Destroy()
            return
        dlg.Destroy()
        response = r_get(self.server_name +
                         '/software/' +
                         self.path_name + '/' +
                         self.common_name + '_' +
                         str(StrictVersion(online_version)) + '.exe', stream=True)
        if not response.ok:
            print(response)
            return
        total_length = response.headers.get('content-length')
        if total_length is None:  # no content length header
            return
        else:
            total_length = int(total_length)  # / 1024
            downloadBytes = total_length / 100
            dlg = wx.ProgressDialog("Download Progress",
                                    "Downloading update now",
                                    parent=self.parent,
                                    style=wx.PD_AUTO_HIDE |
                                    wx.PD_CAN_ABORT |
                                    wx.PD_REMAINING_TIME)
            temp_folder = os.environ.get('temp')
            temp_file = (os.path.join(temp_folder,
                         self.common_name + '_' +
                         str(StrictVersion(online_version)) +
                         '.exe'))
            with open(temp_file, 'wb') as handle:

                count = 0
                for data in response.iter_content(downloadBytes):
                    if data:
                        count += 1
                        if count >= 100:
                            count = 99
                        handle.write(data)
                        (cancel, skip) = dlg.Update(count, "Downloaded " + str(downloadBytes * count / 1024) + " of " + str(total_length / 1024) + "KB")
                        if not cancel:
                            response.close()

            dlg.Destroy()
        if not cancel:
            dlg = wx.MessageDialog(
                parent=self.parent,
                message='Download Cancelled\r\r' +
                'If you want to run the update again, please restart program.',
                caption='Update program cancelled',
                style=wx.OK)

            dlg.ShowModal()
            return
        self.install_update(online_version, temp_file)

    def install_update(self, online_version, temp_file):
        """Installs the downloaded update"""
        dlg = wx.MessageDialog(
            parent=self.parent,
            message='Do you want to update to version ' +
                    str(StrictVersion(online_version)) + ' now?',
            caption='Update program',
            style=wx.OK | wx.CANCEL)

        if dlg.ShowModal() == wx.ID_OK:
            os.startfile(temp_file)
            self.parent.Destroy()
