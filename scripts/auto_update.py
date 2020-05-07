from requests import get as r_get
from distutils.version import StrictVersion
from threading import Thread
from pydispatch import dispatcher


class AutoUpdate(Thread):
    def __init__(self, server_url="http://magicsoftware.ornear.com", program_name="", program_version=""):
        Thread.__init__(self)
        self.server_url = server_url
        self.program_name = program_name  # "Magic Amino Configurator"
        self.program_version = program_version  # "v0.0.3"

    def run(self):
        """Checks on line for updates"""
        try:
            update_url = f'{self.server_url}/updates/{"_".join(self.program_name.lower().split())}/current_version'
            print('update url: ', update_url)
            webpage = r_get(update_url)
            # webpage.raise_for_status()
            online_version = webpage.text
            if StrictVersion(online_version[1:]) > StrictVersion(self.program_version[1:]):
                # print('requires update')
                url = f'{self.server_url}/updates/{"_".join(self.program_name.lower().split())}'
                self.send(message='update', url=url)
            else:
                # print('no update')
                # self.send(message='no update')
                return
        except Exception as error:
            print("Error in update_check: ", error)
            return

    def send(self, message, url=None):
        """Sends the result of the check"""
        dispatcher.send(signal="Software Update", message=message, url=url)


def main():
    test = AutoUpdate(server_url="http://magicsoftware.ornear.com", program_name="Magic DXLink Configurator", program_version="v0.0.1")
    test.start()
    test.join()


if __name__ == '__main__':
    main()
