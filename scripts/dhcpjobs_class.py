# from pydispatch import dispatcher
from threading import Thread
import datetime
from netaddr import IPNetwork
# import subprocess
# import time
try:
    from scripts import datastore
except Exception:
    try:
        import datastore
    except Exception:
        pass
    pass


class DHCPjobs(Thread):

    def __init__(self, parent, queue):
        Thread.__init__(self)
        self.queue = queue
        self.parent = parent

    def run(self):
        while True:
            # gets the job from the queue
            job = self.queue.get()
            getattr(self, job[0])(job)

            # send a signal to the queue that the job is done
            self.queue.task_done()

    def incoming_dhcp(self, job):
        hostname, mac_address, ip_address = job[1]
        # print(job[1])

        incoming_time = datetime.datetime.now()
        if bool(self.parent.preferences.amx_only_filter):
            if mac_address[0:8] != '00:60:9f':
                # print('not amx mac')
                obj = datastore.DXLinkUnit(hostname=hostname, mac_address=mac_address, ip_address=ip_address)
                self.parent.dhcp_on_status_bar(obj, incoming_time)
                return
        if self.parent.preferences.subnet_filter_enable:
            if ip_address not in IPNetwork(self.parent.preferences.subnet_filter):
                # print('no subnet')
                obj = datastore.DXLinkUnit(hostname=hostname, mac_address=mac_address, ip_address=ip_address)
                self.parent.dhcp_on_status_bar(obj, incoming_time)
                return

        # Check if duplicate in list
        duplicate_list = []
        for obj in self.parent.main_list.GetObjects():
            # print('comparing: ', obj.mac_address, mac_address, ' is equal: ', obj.mac_address == mac_address, ' these are repr: ', repr(obj.mac_address), repr(mac_address))
            if obj.mac_address == mac_address:
                # print('duplicate: ', mac_address)
                duplicate_list.append(obj)

        # print('Duplicate list: ', duplicate_list)
        # Add or update list
        if duplicate_list != []:
            # remove duplicates
            if len(duplicate_list) > 1:
                for item in duplicate_list[1:]:
                    self.parent.main_list.RemoveObject(item)
            # update duplicate with new info
            obj = duplicate_list[0]
            obj.ip_address = ip_address
            obj.hostname = hostname
            obj.arrival_time = incoming_time

        else:
            # new item
            obj = datastore.DXLinkUnit(hostname=hostname, mac_address=mac_address, ip_address=ip_address, arrival_time=incoming_time)
            self.parent.main_list.AddObject(obj)
            self.parent.set_status((obj, "DHCP"))

        if obj.hostname[:2] == 'DX':
            # Need to check if we have updated DXLink device recently
            # print(incoming_time - obj.last_status)
            # print(incoming_time - obj.last_status < datetime.timedelta(seconds=2))
            if (incoming_time - obj.last_status) < datetime.timedelta(seconds=2):
                # print('no check')
                pass
            else:
                # print('checking')
                obj.last_status = incoming_time
                self.parent.telnet_job_queue.put(['get_config_info', obj, self.parent.preferences.telnet_timeout])
        self.parent.dhcp_on_status_bar(obj, incoming_time)
        self.parent.main_list.Refresh()
        self.parent.save_main_list()
        self.parent.play_sound()
