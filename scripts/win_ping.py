from threading import Thread
import subprocess
import datetime
from pydispatch import dispatcher


class WinPing(Thread):

    def __init__(self, obj):
        self.obj = obj
        self.shutdown = False
        dispatcher.connect(self.shutdown_signal, signal="Shutdown", sender=dispatcher.Any)
        dispatcher.connect(self.shutdown_signal, signal="Ping Shutdown", sender=dispatcher.Any)
        Thread.__init__(self)

    def run(self):
        """Ping devices constantly for troubleshooting"""
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        ping = subprocess.Popen(['ping', self.obj.ip_address, '-t'], shell=False,
                                stdout=subprocess.PIPE, startupinfo=startupinfo)
        while not self.shutdown:
            for line in iter(ping.stdout.readline, ''):
                result = line.rstrip()
                # print(result)
                if len(result) < 10:
                    continue
                if result == b'':
                    continue
                elif result == b'\n':
                    continue
                elif result[:7] == b'Pinging':
                    continue

                elif result.split()[-1] == b'unreachable.' or result == b'Request timed out.':
                    success = 'No'
                    ms_delay = "N/A"
                    data = (self.obj, [datetime.datetime.now(), ms_delay, success])

                elif result.split()[-1][:3] == b'TTL':
                    temp = result.split()[-2].decode()
                    ms_delay = ''.join([str(s) for s in temp if s.isdigit()])
                    success = 'Yes'
                    data = (self.obj, [datetime.datetime.now(), ms_delay, success])

                else:
                    success = 'No'
                    ms_delay = "N/A"
                    data = (self.obj, [datetime.datetime.now(), ms_delay, success])
                if not self.shutdown:
                    dispatcher.send(signal="Incoming Ping", sender=self, data=data)
                else:
                    break
            # print 'keeprunnning: ', self.keeprunning
        # print('attempting kill')
        ping.kill()

    def shutdown_signal(self, signal):
        self.shutdown = True


class TempUnit:
    count = 0

    def __init__(self):
        self.__class__.count += 1
        self.count = self.__class__.count
        self.ip_address = f'192.168.57.{self.count}'


def incoming(sender, data):
    print(sender, data)


def main():
    dispatcher.connect(incoming, signal="Incoming Ping", sender=dispatcher.Any)
    fakeunits = []
    for i in range(100):
        unit = TempUnit()
        fakeunits.append(unit)

    threads = []
    for unit in fakeunits:
        test = WinPing(obj=unit)
        test.setDaemon(True)
        test.start()
        threads.append(test)
    import time
    time.sleep(5)
    # for item in threads:
    #     item.shutdown = True
    dispatcher.send(signal="Shutdown")
    for item in threads:
        item.join()


if __name__ == "__main__":
    main()
