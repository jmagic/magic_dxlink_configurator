import threading 
import subprocess

class TelnetToThread(threading.Thread):

    def __init__(self, parent, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.parent = parent

    def run(self):
        while True:
            # gets the job from the queue
            obj = self.queue.get()

            if self.parent.os_type == 'nt':
                
                subprocess.call((self.parent.path + self.parent.telnet_client + " " + obj.ip))
            if self.parent.os_type == 'posix':
                subprocess.call(('telnet', obj.ip)) 

 
########################################################################

