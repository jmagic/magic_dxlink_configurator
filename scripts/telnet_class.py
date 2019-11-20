""" Telnets to devices to preform tasks"""

import telnetlib
from pydispatch import dispatcher
from threading import Thread
import datetime
import subprocess
# import serial
# import io
import time
from dataclasses import dataclass, field


@dataclass
class MSEValues:
    report_time: datetime = datetime.datetime.now()
    mse: list = field(default_factory=list)
    obj: object = None


class Telnetjobs(Thread):

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

########################################################################
    def establish_telnet(self, ip_address):
        """Creates the telnet instance"""
        telnet_session = telnetlib.Telnet(ip_address, 23, 5)
        telnet_session.set_option_negotiation_callback(self.call_back)
        return telnet_session

    def call_back(self, sock, cmd, opt):
        """ Turns on server side echoing"""
        if opt == telnetlib.ECHO and cmd in (telnetlib.WILL, telnetlib.WONT):
            sock.sendall(telnetlib.IAC + telnetlib.DO + telnetlib.ECHO)

    def get_config_info(self, job):
        """Gets serial number, firmware from device"""

        obj = job[1]
        self.set_status(obj, "Connecting")
        try:
            telnet_session = self.establish_telnet(obj.ip_address)
            telnet_session.read_until(b'Welcome to', int(job[2]))
            intro = telnet_session.read_until(b'>', int(job[2])).split()
            obj.model = intro[0].decode()
            obj.firmware = intro[1].decode()
            telnet_session.write(b'get sn \r')
            telnet_session.read_until(b'Number:', int(job[2]))
            obj.serial = telnet_session.read_until(b'>', int(job[2])).split()[0].decode()

            telnet_session.write(b'get device \r')
            telnet_session.read_until(b'Value:', int(job[2]))

            obj.device = telnet_session.read_until(b'>', int(job[2])).split()[0].decode()

            telnet_session.write(b'get ip \r')
            telnet_session.read_until(b'HostName:', int(job[2]))
            ip_host = telnet_session.read_until(b'Type:').decode().split()
            if len(ip_host) == 1:
                obj.hostname = ''
            else:
                obj.hostname = ' '.join(ip_host[:-1])
            ip_type = telnet_session.read_until(b'IP').split()

            if ip_type[0] == b"Static":
                obj.ip_type = "s"
            if ip_type[0] == b"DHCP":
                obj.ip_type = "d"
            ip_subnet = telnet_session.read_until(b'Gateway').split()
            obj.subnet = ip_subnet[-2].decode()
            ip_gateway = telnet_session.read_until(b'MAC').split()
            obj.gateway = ip_gateway[-2].decode()
            ip_mac = telnet_session.read_until(b'>', int(job[2])).split()
            obj.mac_address = ip_mac[1].decode()
            self.get_connection(obj, telnet_session, int(job[2]))

            telnet_session.write(b'exit\r')
            telnet_session.close()
            self.set_status(obj, "Success")
        except (IOError, Exception) as error:
            self.error_processing(obj, error)

    def reset_factory(self, job):
        """Sets unit to factory defaults"""

        obj = job[1]
        self.set_status(obj, "Connecting")
        try:
            telnet_session = self.establish_telnet(obj.ip_address)
            telnet_session.read_until(b'>', int(job[2]))
            telnet_session.write(b'reset factory\r')
            telnet_session.read_until(b'>', int(job[2]))
            telnet_session.close()

            self.set_status(obj, "Success")
        except IOError as error:
            self.error_processing(obj, error)

    def set_watchdog(self, job):
        """Enable or disables watchdog"""

        obj = job[1]
        enable = job[3]
        self.set_status(obj, "Connecting")
        try:
            telnet_session = self.establish_telnet(obj.ip_address)
            telnet_session.read_until(b'>', int(job[2]))
            if enable:
                telnet_session.write(b'WD ON\r')
            else:
                telnet_session.write(b'WD OFF\r')
            telnet_session.read_until(b'>', int(job[2]))
            telnet_session.write(b'reboot \r')
            telnet_session.read_until(b'Rebooting....', int(job[2]))
            telnet_session.close()

            self.set_status(obj, "Success")
        except IOError as error:
            self.error_processing(obj, error)

    def reboot(self, job):

        obj = job[1]
        self.set_status(obj, "Connecting")
        # try:
        telnet_session = self.establish_telnet(obj.ip_address)
        telnet_session.read_until(b'>', int(job[2]))
        telnet_session.write(b'reboot\r')
        telnet_session.read_until(b'Rebooting....', int(job[2]))
        telnet_session.close()

        self.set_status(obj, "Success")

        # except Exception as error:
        #     self.error_processing(obj, error)

    def set_device_config(self, job):

        # print job
        obj = job[1]
        delay = int(job[2])
        setdhcp = job[3]
        hostname = job[4]
        # ip_org = job[5]
        ip_new = job[6]
        subnet = job[7]
        gateway = job[8]
        conn_type = job[9]
        master_number = job[10]
        master = job[11]
        device = job[12]
        self.set_status(obj, "Connecting")
        try:
            if setdhcp:

                telnet_session = self.establish_telnet(obj.ip_address)
                telnet_session.read_until(b'>', delay)
                telnet_session.write(b'set ip \r')
                telnet_session.read_until(b'Name:', delay)
                telnet_session.write(hostname.encode('ascii') + b'\r')
                telnet_session.read_until(b'Enter:', delay)
                telnet_session.write(b'd\r')
                telnet_session.read_until(b'Enter', delay)
                telnet_session.write(b'y\r')
                telnet_session.read_until(b'>', delay)

            else:

                telnet_session = self.establish_telnet(obj.ip_address)
                telnet_session.read_until(b'>', delay)
                telnet_session.write(b'set ip \r')
                telnet_session.read_until(b'Name:', delay)
                telnet_session.write(hostname.encode('ascii') + b'\r')
                telnet_session.read_until(b'Enter:', delay)
                telnet_session.write(b's\r')
                telnet_session.read_until(b'Address:', delay)
                telnet_session.write(ip_new.encode('ascii') + b'\r')
                telnet_session.read_until(b'Mask:', delay)
                telnet_session.write(subnet.encode('ascii') + b'\r')
                telnet_session.read_until(b'IP:', delay)
                telnet_session.write(gateway.encode('ascii') + b'\r')
                telnet_session.read_until(b'Enter ->', delay)
                telnet_session.write(b'y\r')
                telnet_session.read_until(b'settings.', delay)
                telnet_session.read_until(b'>', delay)

            if conn_type == "TCP" or conn_type == "UDP":

                telnet_session.write(b'set connection\r')
                telnet_session.read_until(b'Enter:', delay)
                if conn_type == "TCP":
                    telnet_session.write(b't\r')
                else:
                    telnet_session.write(b'u\r')
                telnet_session.read_until(b'URL:', delay)
                telnet_session.write(master.encode('ascii') + b'\r')
                telnet_session.read_until(b'Port:', delay)
                telnet_session.write(b'\r')
                telnet_session.read_until(b'User:', delay)
                telnet_session.write(b'\r')
                telnet_session.read_until(b'Password:', delay)
                telnet_session.write(b'\r')
                telnet_session.read_until(b'Password:', delay)
                telnet_session.write(b'\r')
                telnet_session.read_until(b'Enter ->', delay)
                telnet_session.write(b'y\r')
                telnet_session.read_until(b'written.', delay)
                telnet_session.read_until(b'>', delay)
                telnet_session.write('set device {}'.format(device).encode('ascii') + b'\r')
                telnet_session.read_until(b'device', delay)
                telnet_session.read_until(b'>', delay)

                telnet_session.write(b'reboot \r')
                telnet_session.read_until(b'Rebooting....', delay)
                telnet_session.close()

                self.set_status(obj, "Success")

            if conn_type == "AUTO":

                telnet_session.write(b'set connection\r')
                telnet_session.read_until(b'Enter:', delay)
                telnet_session.write(b'a\r')
                telnet_session.read_until(b'Number:', delay)
                telnet_session.write(master_number.encode('ascii') + b'\r')
                telnet_session.read_until(b'Port:', delay)
                telnet_session.write(b'\r')
                telnet_session.read_until(b'User:', delay)
                telnet_session.write(b'\r')
                telnet_session.read_until(b'Password:', delay)
                telnet_session.write(b'\r')
                telnet_session.read_until(b'Password:', delay)
                telnet_session.write(b'\r')
                telnet_session.read_until(b'Enter ->', delay)
                telnet_session.write(b'y\r')
                telnet_session.read_until(b'written.', delay)
                telnet_session.read_until(b'>', delay)
                telnet_session.write('set device {}'.format(device).encode('ascii') + b'\r')
                telnet_session.read_until(b'device', delay)
                telnet_session.read_until(b'>', delay)
                telnet_session.write(b'reboot\r')
                telnet_session.read_until(b'Rebooting....', delay)
                telnet_session.close()

                self.set_status(obj, "Success")

            if conn_type == "NDP":
                telnet_session.write(b'set connection\r')
                telnet_session.read_until(b'Enter:', delay)
                telnet_session.write(b'n\r')
                telnet_session.read_until(b'Port:', delay)
                telnet_session.write(b'\r')
                telnet_session.read_until(b'User:', delay)
                telnet_session.write(b'\r')
                telnet_session.read_until(b'Password:', delay)
                telnet_session.write(b'\r')
                telnet_session.read_until(b'Password:', delay)
                telnet_session.write(b'\r')
                telnet_session.read_until(b'Enter ->', delay)
                telnet_session.write(b'y\r')
                telnet_session.read_until(b'written.', delay)
                telnet_session.read_until(b'>', delay)
                telnet_session.write('set device {}'.format(device) + b'\r')
                telnet_session.read_until(b'device', delay)
                telnet_session.read_until(b'>', delay)
                telnet_session.write(b'reboot\r')
                telnet_session.read_until(b'Rebooting....', delay)
                telnet_session.close()

                self.set_status(obj, "Success")

        except Exception as error:
            self.error_processing(obj, error)

    def factory_av(self, job):
        """Sets unit audio visual to factory defaults"""
        obj = job[1]
        self.set_status(obj, "Connecting")

        try:
            telnet_session = self.establish_telnet(obj.ip_address)

            telnet_session.read_until(b'>', int(job[2]))
            self.get_connection(obj, telnet_session, int(job[2]))

            command = f"send_command {obj.device}:1:{obj.system},\"\'FACTORYAV\'\""
            telnet_session.write(command.encode('ascii') + b'\r')
            telnet_session.read_until(b'Sending', int(job[2]))
            result_raw = telnet_session.read_until(b'>', int(job[2]))
            if result_raw.split()[0] != b'command:':
                raise Exception('Command not sent')
            telnet_session.write(b'reboot \r')
            telnet_session.read_until(b'Rebooting....', int(job[2]))
            telnet_session.close()

            self.set_status(obj, "Success")

        except Exception as error:
            self.error_processing(obj, error)

    # def get_dipswitch(self, job):
    #     """Gets the dipswitch values"""
    #     obj = job[1]
    #     self.set_status(obj, "Connecting")
    #     try:
    #         telnet_session = self.establish_telnet(obj.ip_address)

    #         telnet_session.read_until(b'>', int(job[2]))
    #         telnet_session.write(b'dipswitch\r')
    #         telnet_session.read_until(b'=', int(job[2]))
    #         result = telnet_session.read_until(b'>', int(job[2]))
    #         for idx, item in enumerate(result.split()):
    #             if item == 'ON':
    #                 obj.dipswitch[idx] = 1
    #             elif item == 'OFF':
    #                 obj.dipswitch[idx] = 0
    #             else:
    #                 obj.dipswitch[idx] = 2  # error

    #         self.set_status(obj, "Success")

    #     except Exception as error:
    #         self.error_processing(obj, error)

    def multiple_send_command(self, job):
        """Sends multiple commands in a single session"""
        obj = job[1]
        command_list = job[3]
        if obj.device == " ":
            device = 0
        else:
            device = obj.device
        if obj.system == " ":
            system = 0
        else:
            system = obj.system

        self.set_status(obj, "Connecting")
        self.notify_send_command_window(obj)
        # try:
        telnet_session = self.establish_telnet(obj.ip_address)
        telnet_session.read_until(b'>', int(job[2]))
        total = len(command_list)
        count = 0
        error = 0
        for command in command_list:
            count += 1
            output = f"send_command {device}:{command[1]}:{system},\"\'{command[0]}\'\""
            telnet_session.write(output.encode('ascii') + b"\r")
            result_raw = telnet_session.read_until(b'>', int(job[2]))
            if result_raw.split()[0] != b'command:':
                dispatcher.send(
                    signal="send_command result",
                    sender=((True, 'Sending ' + result_raw.decode()[:-1])))
                self.set_status(
                    obj, ('Sent ' + str(count) + ' of ' + str(total)))
                self.notify_send_command_window(obj)
            else:
                error += 1
                dispatcher.send(signal="send_command result",
                                sender=((False, 'Failed to send command')))

        telnet_session.close()
        if not error:
            self.set_status(obj, 'Success')
            self.notify_send_command_window(obj)
        else:
            self.set_status(obj, 'Failed')
            self.notify_send_command_window(obj)
        # except Exception as error:
        #     self.error_processing(obj, error)
        #     self.notify_send_command_window(obj)

    def send_command(self, job):

        obj = job[1]
        command_sent = job[3]
        self.set_status(obj, "Connecting")

        # try:
        telnet_session = self.establish_telnet(obj.ip_address)

        telnet_session.read_until(b'>', int(job[2]))
        # self.get_connection(obj, telnet_session, int(job[2]))

        command = command_sent.encode('ascii') + b"\r"
        # print command
        telnet_session.write(command)
        telnet_session.read_until(b'Sending', int(job[2]))
        result_raw = telnet_session.read_until(b'>', int(job[2]))
        # print result_raw.split()
        if result_raw.split()[0] != b'command:':
            raise Exception('Command not sent')
        else:
            dispatcher.send(signal="send_command result",
                            sender=(('Sending ' + str(result_raw)[:-1])))

        telnet_session.close()

        self.set_status(obj, "Success")
        self.notify_send_command_window(obj)

        # except Exception as error:
        #     self.error_processing(obj, error)

    def turn_on_leds(self, job):
        """Turns on LEDs"""

        obj = job[1]
        self.set_status(obj, "Connecting")
        try:
            telnet_session = self.establish_telnet(obj.ip_address)
            telnet_session.read_until(b'>', int(job[2]))
            telnet_session.write(b'led on \r')
            telnet_session.read_until(b'ON', int(job[2]))
            telnet_session.close()

            self.set_status(obj, "Success")

        except Exception as error:
            self.error_processing(obj, error)

    def turn_off_leds(self, job):
        """Turns off leds"""
        obj = job[1]
        self.set_status(obj, "Connecting")
        try:
            telnet_session = self.establish_telnet(obj.ip_address)
            telnet_session.read_until(b'>', int(job[2]))
            telnet_session.write(b'led off \r')
            telnet_session.read_until(b'OFF', int(job[2]))
            telnet_session.close()

            self.set_status(obj, "Success")

        except Exception as error:
            self.error_processing(obj, error)

    def get_dxlink_mse(self, job):
        """Gathers MSE values"""
        # print('in get dxlink mse')
        obj = job[1]
        self.set_status(obj, "Connecting")
        try:

            telnet_session = self.establish_telnet(obj.ip_address)
            telnet_session.read_until(b'>', 2)
            # telnet_session.read_very_eager()
            self.set_status(obj, "MSE")
            while obj.mac_address in self.parent.mse_active_list:
                my_values = MSEValues(obj=obj)
                telnet_session.write(b'show vs100 stats \r')
                telnet_session.read_until(b'MSE(db)')
                stats = telnet_session.read_until(b'VS100').split()
                for i in range(len(stats)):
                    if stats[i] == b"ChA:":
                        my_values.mse.append(int(stats[i + 1][:-1].decode()))
                        my_values.mse.append(int(stats[i + 3][:-1].decode()))
                        my_values.mse.append(int(stats[i + 5][:-1].decode()))
                        my_values.mse.append(int(stats[i + 7].decode()))
                if my_values.mse != []:
                    dispatcher.send(signal="Incoming MSE", data=my_values)

                telnet_session.read_until(b'>', 2)
            self.set_status(obj, "Success")

        except Exception as error:
            time.sleep(2)  # wait for gui to start
            # print('Telnet MSE error: ', error)
            dispatcher.send(signal="MSE error", sender=obj.mac_address)
            self.set_status(obj, "Failed")

    def ping(self, job):
        """Ping devices constantly for troubleshooting"""
        obj = job[1]
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        ping = subprocess.Popen(['ping', obj.ip_address, '-t'], shell=False,
                                stdout=subprocess.PIPE, startupinfo=startupinfo)
        while self.parent.ping_active:
            for line in iter(ping.stdout.readline, ''):
                result = line.rstrip()
                if len(result) < 10:
                    continue
                if result == '':
                    continue
                elif result == '\n':
                    continue
                elif result[:7] == 'Pinging':
                    continue

                elif result.split()[-1] == 'unreachable.' or result == 'Request timed out.':
                    success = 'No'
                    ms_delay = "N/A"
                    data = (obj, [datetime.datetime.now(), ms_delay, success])
                    if self.parent.ping_active:
                        dispatcher.send(signal="Incoming Ping", sender=data)

                elif result.split()[-1][:3] == 'TTL':
                    temp = result.split()[-2]
                    ms_delay = ''.join([str(s) for s in temp if s.isdigit()])
                    success = 'Yes'
                    data = (obj, [datetime.datetime.now(), ms_delay, success])
                    if self.parent.ping_active:
                        dispatcher.send(signal="Incoming Ping", sender=data)
                else:
                    success = 'No'
                    ms_delay = "N/A"
                    data = (obj, [datetime.datetime.now(), ms_delay, success])
                    if self.parent.ping_active:
                        dispatcher.send(signal="Incoming Ping", sender=data)
                if not self.parent.ping_active:
                    break
        ping.kill()

    def get_connection(self, obj, session, timeout):
        """ Function to get connection information """
        session.write(b'get connection \r')
        session.read_until(b'Mode:', timeout)
        connection_info = session.read_until(b'>', timeout).split()
        if connection_info[0] == b'NDP' or connection_info[0] == b'AUTO':
            if connection_info[7] == b'(n/a)' or connection_info[3] == b'(not':
                obj.master = 'not connected'
                obj.system = '0'
            else:
                obj.master = connection_info[6].decode()
                obj.system = connection_info[3].decode()

        if connection_info[0] == b'TCP' or connection_info[0] == b'UDP':
            if connection_info[8] == b'(n/a)':
                obj.master = 'not connected'
                obj.system = '0'
            else:
                obj.master = connection_info[7].decode()
                obj.system = connection_info[4].decode()

    def set_status(self, obj, status):
        """Updates progress in main"""
        data = (obj, status)
        dispatcher.send(signal="Status Update", sender=data)

    def notify_send_command_window(self, obj):
        """updates send_command window"""
        dispatcher.send(signal="Update Window", sender=obj)

    def error_processing(self, obj, error):
        """Send notification of error to main"""

        if str(error) == 'Not an AMX device':
            data = (obj, 'Warning, not a recognized dxlink device')
        else:
            data = (obj, str(error))
        dispatcher.send(signal="Collect Errors", sender=data)
