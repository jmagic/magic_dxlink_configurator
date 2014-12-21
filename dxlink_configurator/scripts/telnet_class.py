""" Telnets to devices to preform tasks"""

import telnetlib
from pydispatch import dispatcher
from threading import Thread
import time
import datetime
import subprocess
import serial
import io


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
        self.communication_started(obj) 
        try:
            telnet_session = self.establish_telnet(obj.ip_address)
            
            telnet_session.read_until('Welcome to', int(job[2]))
            intro = telnet_session.read_until('>', int(job[2])).split()
            obj.model = intro[0]
            obj.firmware = intro[1]
            telnet_session.write('get sn \r')
            telnet_session.read_until('Number:', int(job[2]))
            obj.serial = telnet_session.read_until('>', int(job[2])).split()[0]

            telnet_session.write('get device \r')
            telnet_session.read_until('Value:', int(job[2]))

            obj.device = telnet_session.read_until('>', int(job[2])).split()[0]

            telnet_session.write('get ip \r')
            telnet_session.read_until('HostName:', int(job[2]))
            ip_host = telnet_session.read_until('Type:').split()
            if len(ip_host) == 1:
                obj.hostname = ''
            else:
                obj.hostname = ' '.join(ip_host[:-1])
            ip_type = telnet_session.read_until('IP').split()

            if ip_type[0] == "Static":
                obj.ip_type = "s"
            if ip_type[0] == "DHCP":
                obj.ip_type = "d"
            ip_subnet = telnet_session.read_until('Gateway').split()
            obj.subnet = ip_subnet[-2]
            ip_gateway = telnet_session.read_until('MAC').split()
            obj.gateway = ip_gateway[-2]
            ip_mac = telnet_session.read_until('>', int(job[2])).split()
            obj.mac_address = ip_mac[1]
            self.get_connection(obj, telnet_session, int(job[2]))

            telnet_session.write('exit')
            telnet_session.close()
            self.communication_success(obj) 
        except (IOError, Exception) as error:
            self.error_processing(obj, error)


    def reset_factory(self, job):
        """Sets unit to factory defaults"""

        obj = job[1]

        try:
            telnet_session = self.establish_telnet(obj.ip_address)
            telnet_session.read_until('>', int(job[2]))
            telnet_session.write('reset factory\r')
            telnet_session.read_until('>', int(job[2]))
            telnet_session.close()

            self.communication_success(obj)

        except IOError, error:
            self.error_processing(obj, error)

    def reboot(self, job):

        obj = job[1]

        try:
            telnet_session = self.establish_telnet(obj.ip_address)
            telnet_session.read_until('>', int(job[2]))
            telnet_session.write('reboot \r')
            telnet_session.read_until('Rebooting....', int(job[2]))
            telnet_session.close()

            self.communication_success(obj)

        except Exception as error:
            self.error_processing(obj, error)


    def set_device_config(self, job):

        #print job
        obj = job[1]
        setdhcp = job[3]
        hostname = job[4]
        #ip_org = job[5]
        ip_new = job[6]
        subnet = job[7]
        gateway = job[8]
        master = job[9]
        device = job[10]

        if setdhcp == True:
            try:
                telnet_session = self.establish_telnet(obj.ip_address)
                telnet_session.read_until('>', int(job[2]))
                telnet_session.write('set ip \r')
                telnet_session.read_until('Name:', int(job[2]))
                telnet_session.write(hostname + '\r')
                telnet_session.read_until('Enter:', int(job[2]))
                telnet_session.write('d\r')
                telnet_session.read_until('Enter', int(job[2]))
                telnet_session.write('y\r')
                telnet_session.read_until('>', int(job[2]))

                telnet_session.write('set connection\r')
                telnet_session.read_until('Enter:', int(job[2]))
                telnet_session.write('t\r')
                telnet_session.read_until('URL:', int(job[2]))
                telnet_session.write(master + '\r')
                telnet_session.read_until('Port:', int(job[2]))
                telnet_session.write('\r')
                telnet_session.read_until('User:', int(job[2]))
                telnet_session.write('\r')
                telnet_session.read_until('Password:', int(job[2]))
                telnet_session.write('\r')
                telnet_session.read_until('Password:', int(job[2]))
                telnet_session.write('\r')
                telnet_session.read_until('Enter ->', int(job[2]))
                telnet_session.write('y\r')
                telnet_session.read_until('written.', int(job[2]))
                telnet_session.read_until('>', int(job[2]))
                telnet_session.write('set device ' + str(device) + '\r')
                telnet_session.read_until('device', int(job[2]))
                telnet_session.read_until('>', int(job[2]))

                telnet_session.write('reboot \r')
                telnet_session.read_until('Rebooting....', int(job[2]))
                telnet_session.close()

                self.communication_success(obj)

            except Exception as error:
                self.error_processing(obj, error)

        else:
            try:
                telnet_session = self.establish_telnet(obj.ip_address)

                telnet_session.read_until('>', int(job[2]))
                telnet_session.write('set ip \r')
                telnet_session.read_until('Name:', int(job[2]))
                telnet_session.write(hostname + '\r')
                telnet_session.read_until('Enter:', int(job[2]))
                telnet_session.write('s\r')
                telnet_session.read_until('Address:', int(job[2]))
                telnet_session.write(ip_new + '\r')
                telnet_session.read_until('Mask:', int(job[2]))
                telnet_session.write(subnet + '\r')
                telnet_session.read_until('IP:', int(job[2]))
                telnet_session.write(gateway + '\r')
                telnet_session.read_until('Enter ->', int(job[2]))
                telnet_session.write('y\r')
                telnet_session.read_until('settings.', int(job[2]))
                telnet_session.read_until('>', int(job[2]))

                telnet_session.write('set connection\r')
                telnet_session.read_until('Enter:', int(job[2]))
                telnet_session.write('t\r')
                telnet_session.read_until('URL:', int(job[2]))
                telnet_session.write(master + '\r')
                telnet_session.read_until('Port:', int(job[2]))
                telnet_session.write('\r')
                telnet_session.read_until('User:', int(job[2]))
                telnet_session.write('\r')
                telnet_session.read_until('Password:', int(job[2]))
                telnet_session.write('\r')
                telnet_session.read_until('Password:', int(job[2]))
                telnet_session.write('\r')
                telnet_session.read_until('Enter ->', int(job[2]))
                telnet_session.write('y\r')
                telnet_session.read_until('written.', int(job[2]))
                telnet_session.read_until('>', int(job[2]))
                telnet_session.write('set device ' + str(device) + '\r')
                telnet_session.read_until('device', int(job[2]))
                telnet_session.read_until('>', int(job[2]))
                telnet_session.write('reboot\r')
                telnet_session.read_until('Rebooting....', int(job[2]))
                telnet_session.close()

                self.communication_success(obj)

            except Exception as error:
                self.error_processing(obj, error)

    def factory_av(self, job):
        """Sets unit audio visual to factory defaults"""
        obj = job[1]

        try:
            telnet_session = self.establish_telnet(obj.ip_address)

            telnet_session.read_until('>', int(job[2]))
            self.get_connection(obj, telnet_session, int(job[2]))

            command = ("send_command " +
                       str(obj.device) + 
                       ":" + 
                       "1" + 
                       ":" + 
                       str(obj.system) + 
                       " , " + 
                       "\"\'FACTORYAV\'\" \r")
            telnet_session.write(command)
            telnet_session.read_until('Sending', int(job[2]))
            result_raw = telnet_session.read_until('>', int(job[2]))
            if result_raw.split()[0] != 'command:':
                raise Exception, ('Command not sent')
            telnet_session.write('reboot \r')
            telnet_session.read_until('Rebooting....', int(job[2]))
            telnet_session.close()

            self.communication_success(obj)

        except Exception as error:
            self.error_processing(obj, error)


    def send_command(self, job):

        obj = job[1]
        command_sent = job[3]

        try:
            telnet_session = self.establish_telnet(obj.ip_address)

            telnet_session.read_until('>', int(job[2]))
            self.get_connection(obj, telnet_session, int(job[2]))

            command = command_sent  + " \r"
            #print command
            telnet_session.write(str(command))
            telnet_session.read_until('Sending', int(job[2]))
            result_raw = telnet_session.read_until('>', int(job[2]))
            if result_raw.split()[0] != 'command:':
                raise Exception, ('Command not sent')
            else:
                dispatcher.send(signal="send_command result", 
                                sender=('Sending' + str(result_raw[:-1])))

            telnet_session.close()

            self.communication_success(obj)

        except Exception as error:
            self.error_processing(obj, error)

    def turn_on_leds(self, job):
        """Turns on LEDs"""

        obj = job[1]
        try:
            telnet_session = self.establish_telnet(obj.ip_address)
            telnet_session.read_until('>', int(job[2]))
            telnet_session.write('led on \r')
            telnet_session.read_until('ON', int(job[2]))
            telnet_session.close()

            self.communication_success(obj)

        except Exception as error:
            self.error_processing(obj, error)


    def turn_off_leds(self, job):
        """Turns off leds"""
        obj = job[1]

        try:
            telnet_session = self.establish_telnet(obj.ip_address)
            telnet_session.read_until('>', int(job[2]))
            telnet_session.write('led off \r')
            telnet_session.read_until('OFF', int(job[2]))
            telnet_session.close()

            self.communication_success(obj)

        except Exception as error:
            self.error_processing(obj, error)

    def get_dxlink_mse(self, job):
        """Gathers MSE values"""
        obj = job[1]
        try:

            telnet_session = self.establish_telnet(obj.ip_address)
            telnet_session.read_until('>', 2)
            #telnet_session.read_very_eager()

            mse = []
            data = []
            while obj.mac_address in self.parent.mse_active_list: 

                telnet_session.write('show vs100 stats \r')
                telnet_session.read_until('MSE(db)')
                stats = telnet_session.read_until('VS100').split()
                for i in range(len(stats)):
                    if stats[i] == "ChA:":
                        data.append(stats[i+1][:-1])
                        data.append(stats[i+3][:-1])
                        data.append(stats[i+5][:-1])
                        data.append(stats[i+7])
                if data != []:
                    mse_time = [datetime.datetime.now(), data]
                    mse.append(mse_time)
                    mse.append(obj.ip_address)
                    mse.append(obj.mac_address)
                    dispatcher.send(signal="Incoming MSE", sender=mse)
                    mse = []
                    data = []

                telnet_session.read_until('>', 2)

        except:
            time.sleep(2) # wait for gui to start
            dispatcher.send(signal="MSE error", sender=obj.mac_address)

    def get_dgx_mse(self, job):
        "Gathers DGX MSE values"
        obj = job[1]

        if len(self.parent.serial_active) == 1:
            try:
                ser = serial.Serial(obj.ip_address, 9600, timeout=.1)
                sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
            except Exception:
                time.sleep(2) # wait for gui to start
                dispatcher.send(signal="MSE error", sender=obj.mac_address)
                return
            sio.write(unicode(str("\x03")))
        
            while self.parent.serial_active != []: 

                sio.flush()
                #print sio.readlines()
                sio.write(unicode(str("show stats \n")))
                sio.flush()
                dgx_output = sio.readlines()
                        
                #Find the cards in the system
                for block in dgx_output:
                    #if block[:-2] == "BCPU6":
                    #print 'block[:-3] == obj.device', block[:-3], obj.device
                    if block[:-3] == "BCPU":
                        card_line_number = dgx_output.index(block)
                        #print card_line_number 
                        # lets count from the BCPU to the MSE value lines by 4's
                        for mse_line in range(card_line_number + 3, 
                                              card_line_number + 16, 4): 
                            if str(dgx_output[mse_line][-10:-2]) != "Unlinked":
                                #print dgx_output[mse_line]
                                bcpu = int(block[-3:-2])
                                #print bcpu
                                if str(dgx_output[mse_line][6:8]) == "RX":
                                    dgx_output[mse_line] = (
                                               dgx_output[mse_line].split()[0] +
                                               " " + dgx_output[mse_line]) 

                                row = []
                                mline = []
                                try:
                                    for mse in [4, 6, 8]:
                                        row.append(str(dgx_output[mse_line]\
                                                           .split()[mse][2:-3]))
                                        #one less no comma on this one
                                        row.append(str(dgx_output[mse_line]\
                                                            .split()[10][2:-2]))
                                except IndexError:
                                    #print "Index error building dgx mse row"
                                    continue
                                #print "row", row
                                if row != []:
                                    mline_time = [datetime.datetime.now(), row]
                                    mline.append(mline_time)
                                    mline.append(('BCPU' + str(bcpu) + '_' + 
                                                   str(dgx_output[mse_line]\
                                                   .split()[0][:3])))
                                    #DGX_BCPU5_Ch1 
                                    mline.append(('BCPU' + str(bcpu) + '_' + 
                                                   str(dgx_output[mse_line]\
                                                   .split()[0][:3])))
                                    #print mline
                                    dispatcher.send(signal="Incoming MSE", 
                                                    sender=mline)
                                    mline = []
                                    row = []
            


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

                elif result.split()[-1] == 'unreachable.' or \
                                 result == 'Request timed out.':
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
        session.write('get connection \r')
        session.read_until('Mode:', timeout)
        connection_info = session.read_until('>', timeout).split()
        if connection_info[0] == 'NDP':
            if connection_info[7] == '(n/a)':
                obj.master = 'not connected'
                obj.system = '0'
            else:
                obj.master = connection_info[6]
                obj.system = connection_info[3]

        if connection_info[0] == 'TCP' or connection_info[0] == 'UDP':
            if connection_info[8] == '(n/a)':
                obj.master = 'not connected'
                obj.system = '0'
            else:
                obj.master = connection_info[7]
                obj.system = connection_info[4]

    def communication_started(self, obj):
        """Updates progress in main"""
        dispatcher.send(signal="Communication Started", sender=obj)

    def communication_success(self, obj):
        """Send notification of success to main"""
        dispatcher.send(signal="Collect Completions", sender=obj)

    def error_processing(self, obj, error):
        """Send notification of error to main"""

        if str(error) == 'Not an AMX device':
            data = (obj, 'Warning, not a recognized dxlink device')
        else:
            data = (obj, str(error))
        dispatcher.send(signal="Collect Errors", sender=data)

