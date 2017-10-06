"""Continuously pings devices for troubleshooting"""

from pydispatch import dispatcher
import datetime
import os
import csv
from . import ping_class


class PingUnit(object):
    """
    Model of the Ping Unit

    Contains the following attributes:
    'hostname','serial','device','mac','thread'
    """
    # ----------------------------------------------------------------------
    def __init__(self, obj, path, logging=False):

        self.obj = obj
        self.ping_data = []
        self.hostname = obj.hostname
        self.serial = obj.serial
        self.ip_address = obj.ip_address
        self.mac_address = obj.mac_address
        self.success = 0
        self.failed = 0
        self.path = path
        self.logging = logging
        self.log = ('device_' +
                    obj.ip_address +
                    '_time_' +
                    datetime.datetime.now().strftime('%H_%M_%S') +
                    '.csv')
        dispatcher.connect(
            self.on_incoming_ping,
            signal="Incoming Ping",
            sender=dispatcher.Any)
        self.thread = self.start_thread(obj)

    def on_incoming_ping(self, sender):
        if sender[0] == self.obj:
            self.ping_data.append(self.set_ping_data(sender[1]))
            if sender[1][2] == 'Yes':
                self.success += 1
            else:
                self.failed += 1
            if self.logging:
                self.save_log()

    def set_ping_data(self, ping_info):
        """Makes a ping data unit"""
        return Ping_Data_Unit(
            ping_info[0],  # .strftime('%H:%M:%S.%f')
            ping_info[1],
            ping_info[2])

    def save_log(self):
        """Save log to a file"""
        log_path = os.path.join(self.path, 'ping_logs')
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        output_file = os.path.join(log_path, self.log)

        with open(output_file, 'ab') as log_file:
            writer_csv = csv.writer(log_file, quoting=csv.QUOTE_ALL)
            row = []
            row.append(str(self.ping_data[-1].ping_time))
            row.append(str(self.ping_data[-1].ms_delay))
            row.append(str(self.ping_data[-1].success))
            writer_csv.writerow(row)

    def start_thread(self, obj):
        """Starts pinging ip_address"""
        ping_thread = ping_class.PingJob(obj)
        ping_thread.setDaemon(True)
        ping_thread.start()
        return ping_thread


class Ping_Data_Unit(object):
    """
    Model of the Ping_Data_Unit

    Contains the following attributes:
    ping_time, ms delay, successful """
    # ----------------------------------------------------------------------
    def __init__(self, ping_time, ms_delay, success):

        self.ping_time = ping_time
        self.ms_delay = ms_delay
        self.success = success


class MultiPing_Model(object):
    def __init__(self, path='.'):
        self.path = path
        self.ping_objects = []
        self.logging = False

    def add_items(self, device_list):
        """Adds new devices to the list"""
        self.clean_up()
        current_ip_addresses = []
        for obj in self.ping_objects:
            current_ip_addresses.append(obj.ip_address)
        for obj in device_list:
            # print 'compare: ', obj.ip_address, current_ip_addresses
            if obj.ip_address not in current_ip_addresses:
                new_obj = PingUnit(obj, self.path, self.logging)
                self.ping_objects.append(new_obj)
        dispatcher.send(signal='Ping Model Update',
                        sender=self.ping_objects)

    def clean_up(self):
        for obj in self.ping_objects:
            if not obj.thread.isAlive():
                try:
                    self.ping_objects.remove(obj)
                except:
                    pass

    def delete(self, item):
        """Removes an item from pinging"""
        item.thread.keeprunning = False

    def reset(self, item):
        """Resets the item"""
        item.ping_data = []
        item.success = 0
        item.failed = 0

    def toggle_logging(self):
        """Toggles logging"""
        if self.logging:
            for item in self.ping_objects:
                item.logging = False
        else:
            for item in self.ping_objects:
                item.logging = True
        self.logging = not self.logging

    def shutdown(self):
        for item in self.ping_objects:
            item.thread.keeprunning = False
        while self.ping_objects:
            self.clean_up()


def main():
    """Run stand alone"""
    pass

if __name__ == '__main__':
    main()
