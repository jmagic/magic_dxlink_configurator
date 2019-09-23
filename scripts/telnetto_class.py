"""Opens a subprocess to launch the telnet client"""
import os
import threading
import subprocess
from pydispatch import dispatcher


class TelnetToThread(threading.Thread):
    """Telnet to thread"""

    def __init__(self, parent, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.parent = parent
        self.prefs = self.parent.preferences

    def run(self):
        while True:
            # gets the job from the queue
            job = self.queue.get()
            obj = job[0]
            task = job[1]
            self.set_status(obj, "Telnet")
            subprocess.call([self.prefs.telnet_client, f'-{task}', obj.ip_address])
            self.set_status(obj, "Success")

    def set_status(self, obj, status):
        """Updates progress in main"""
        data = (obj, status)
        dispatcher.send(signal="Status Update", sender=data)
