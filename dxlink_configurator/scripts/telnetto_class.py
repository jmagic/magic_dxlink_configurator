import threading 
import subprocess
import os

class telnet_to_thread(threading.Thread):

    def __init__(self, parent, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.parent = parent

    def run(self):
        while True:
            # gets the job from the queue
            obj = self.queue.get()

            if os.name == 'nt':
                
                subprocess.call((self.parent.path + self.parent.telnet_client +
                                  " " + obj.ip_address))
            if os.name == 'posix':
                subprocess.call(('telnet', obj.ip_address)) 

 
########################################################################

