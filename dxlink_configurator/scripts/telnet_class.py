import telnetlib
from pydispatch import dispatcher
from threading import Thread
import time
import datetime
import subprocess

class Telnetjobs(Thread):

    def __init__(self, parent, queue):
        Thread.__init__(self)
        self.queue = queue
        self.parent = parent

    def run(self):
        while True:
            # gets the job from the queue
            job = self.queue.get()

            # download the file
            #print job

            self.type = job[0]
            self.timeout = int(job[2])

            if self.type == "GetTelnetInfo":
                self.GetTelnetInfo(job)
            elif self.type == "SetDHCP":
                self.SetDHCP(job)
            elif self.type == "SetMaster":
                self.SetMaster(job)
            elif self.type == "SetFactory":
                self.SetFactory(job)
            elif self.type == "SetReboot":
                self.SetReboot(job)
            elif self.type == "SetStatic":
                self.SetStatic(job)
            elif self.type == "SetSerialMAC":
                self.SetSerialMAC(job)
            elif self.type == "DeviceConfig":
                self.SetDeviceConfig(job)
            elif self.type == "FactoryAV":
                self.FactoryAV(job)
            elif self.type == "SendCommand" :
                self.SendCommand(job)
            elif self.type == "TurnOnLED" :
                self.SetTurnOnLED(job)
            elif self.type == "TurnOffLED" :
                self.SetTurnOffLED(job)
            elif self.type == "MSE" :
                self.SetMSE(job)
            elif self.type == "Ping" :
                self.SetPing(job)

            # send a signal to the queue that the job is done
            self.queue.task_done()

########################################################################
    def GetTelnetInfo(self, job):

        obj = job[1]
        ip = obj.ip_address

        try:
            tn = telnetlib.Telnet(ip, 23, self.timeout)

            tn.read_until ('Welcome to' , self.timeout)

            intro = tn.read_very_eager().split()

            #if intro[0] == 'DXLINK':
            obj.model =  intro[0]
            obj.firmware = intro[1]


            tn.write ('get sn \r')
            tn.read_until ('Number:', self.timeout)

            obj.serial = tn.read_very_eager().split()[0]

            tn.write ('get device \r')
            tn.read_until('Value:', self.timeout)

            obj.device = tn.read_very_eager().split()[0]

            tn.write ('get ip \r')
            tn.read_until('HostName:', self.timeout)
            ip_info = tn.read_very_eager().split()
            if ip_info[0] == "Type:":
                obj.hostname = " "
                ip_info.insert(0, " ")
            else:
                obj.hostname = ip_info[0]

            if ip_info[2] == "Static":
                obj.ip_type = "s"
            if ip_info[2] == "DHCP":
                obj.ip_type = "d"
            obj.subnet = ip_info[8]
            obj.gateway = ip_info[11]
            obj.mac_address = ip_info[14]


            #tn.read_until('>')
            tn.write ('get connection \r')
            tn.read_until('Mode:', self.timeout )
            connection_info = tn.read_very_eager().split()
            #print connection_info
            if connection_info[0] == 'NDP':
                if connection_info[7] == '(n/a)':
                    obj.master = 'not connected'
                    obj.system = '0'
                else:
                    obj.master = connection_info[7]
                    obj.system = connection_info[4]

            if connection_info[0] == 'TCP':
                if connection_info[8] == '(n/a)':
                    obj.master = 'not connected'
                    obj.system = '0'
                else:
                    obj.master = connection_info[7]
                    obj.system = connection_info[4]

            #tn.read_until('>')

            '''if intro[0] == 'NXD-430':
                obj.model = intro[0]
                obj.firmware = intro[1]

                tn.write ('get sn \r')
                tn.read_until ('Number:', self.timeout )
                obj.serial = tn.read_very_eager().split()[0]

            if intro[0] == 'NetLinx':
                obj.model = intro[0]
                obj.firmware = intro[1]

                tn.write ('show system \r')
                system_info = tn.read_until('Address', self.timeout )
                obj.serial = system_info.split()[23].split("'")[1]
                #print test'''

            tn.write ('exit')
            tn.close()


            self.communicationSuccess(obj)

        except Exception, error:
            self.errorProcessing(obj,error)

    def SetMaster(self, job):

        obj = job[1]
        master = job[3]
        device = job[4]
        ip = obj.ip_address
        #print master, device, ip

        try:

            tn = telnetlib.Telnet(ip,23,self.timeout)

            tn.read_until('>', self.timeout)
            tn.write ('set connection\r')
            tn.read_until('Enter:', self.timeout )
            tn.write ('t\r')
            tn.read_until('URL:', self.timeout )
            tn.write ( master + '\r')
            tn.read_until('Port:', self.timeout )
            tn.write ('\r')
            tn.read_until('User:', self.timeout )
            tn.write ('\r')
            tn.read_until('Password:', self.timeout )
            tn.write ('\r')
            tn.read_until('Password:', self.timeout )
            tn.write ('\r')
            tn.read_until('Enter ->', self.timeout )
            tn.write ('y\r')
            tn.read_until('written.', self.timeout)
            tn.read_until('>', self.timeout)
            tn.write ('set device ' + str(device) + '\r')
            tn.read_until('device', self.timeout)
            tn.read_until('>', self.timeout)
            tn.write ('reboot\r')
            tn.read_until('Rebooting....', self.timeout)
            tn.close()

            self.communicationSuccess(obj)

        except Exception, error:
            self.errorProcessing(obj,error)


    def SetDHCP(self, job):

        obj = job[1]
        ip = obj.ip_address

        try:
            tn = telnetlib.Telnet(ip,23, self.timeout)
            tn.read_until('>', self.timeout)
            tn.write ('set ip \r')
            tn.read_until('Name:', self.timeout)
            tn.write ('\r')
            tn.read_until('Enter:', self.timeout)
            tn.write ('d\r')
            tn.read_until('Enter', self.timeout)
            tn.write ('y\r')
            tn.read_until('>', self.timeout )
            tn.write ('reboot \r')
            tn.read_until('Rebooting....')
            tn.close()

            self.communicationSuccess(obj)

        except Exception, error:
            self.errorProcessing(obj,error)



    def SetFactory(self, job):

        obj = job[1]
        ip = obj.ip_address

        try:
            tn = telnetlib.Telnet(ip,23, self.timeout)
            tn.read_until('>', self.timeout )
            tn.write ('reset factory\r')
            tn.read_until('>', self.timeout )
            tn.close()

            self.communicationSuccess(obj)

        except Exception, error:
            self.errorProcessing(obj,error)

    def SetReboot(self, job):

        obj = job[1]
        ip = obj.ip_address

        try:
            tn = telnetlib.Telnet(ip,23, self.timeout)
            tn.read_until('>', self.timeout)
            tn.write ('reboot \r')
            tn.read_until('Rebooting....', self.timeout )
            tn.close()

            self.communicationSuccess(obj)

        except Exception, error:
            self.errorProcessing(obj,error)

    def SetStatic(self, job):

        #print job
        obj = job[1]
        hostname = job[3]
        ip_org = job[4]
        ip_new = job[5]
        subnet = job[6]
        gateway = job[7]

        try:
            tn = telnetlib.Telnet(ip_org,23,self.timeout)

            tn.read_until('>',self.timeout)
            tn.write ('set ip \r')
            tn.read_until('Name:',self.timeout)
            tn.write ( hostname + '\r')
            tn.read_until('Enter:',self.timeout)
            tn.write ('s\r')
            tn.read_until('Address:',self.timeout)
            tn.write ( ip_new + '\r')
            tn.read_until('Mask:',self.timeout)
            tn.write ( subnet + '\r')
            tn.read_until('IP:',self.timeout)
            tn.write ( gateway + '\r')
            tn.read_until('Enter ->',self.timeout)
            tn.write ('y\r')
            tn.read_until('settings.',self.timeout)
            tn.read_until('>',self.timeout)
            tn.write ('reboot\r')
            tn.read_until('Rebooting....',self.timeout)
            tn.close()

            self.communicationSuccess(obj)

        except Exception, error:
            self.errorProcessing(obj,error)

    def SetDeviceConfig(self, job):

        #print job
        obj = job[1]
        setdhcp = job[3]
        hostname = job[4]
        ip_org = job[5]
        ip_new = job[6]
        subnet = job[7]
        gateway = job[8]
        master = job[9]
        device = job[10]

        if setdhcp == True:
            try:
                tn = telnetlib.Telnet(ip_org,23,self.timeout)
                tn.read_until('>',self.timeout)
                tn.write ('set ip \r')
                txt = tn.read_until('Name:',self.timeout)
                #if txt != 'Name:':
                #    raise Exception('Not DXLink')
                tn.write ( hostname + '\r')
                tn.read_until('Enter:',self.timeout)
                tn.write ('d\r')
                tn.read_until('Enter',self.timeout)
                tn.write ('y\r')
                tn.read_until('>',self.timeout)

                tn.write ('set connection\r')
                tn.read_until('Enter:', self.timeout )
                tn.write ('t\r')
                tn.read_until('URL:', self.timeout )
                tn.write ( master + '\r')
                tn.read_until('Port:', self.timeout )
                tn.write ('\r')
                tn.read_until('User:', self.timeout )
                tn.write ('\r')
                tn.read_until('Password:', self.timeout )
                tn.write ('\r')
                tn.read_until('Password:', self.timeout )
                tn.write ('\r')
                tn.read_until('Enter ->', self.timeout )
                tn.write ('y\r')
                tn.read_until('written.',self.timeout)
                tn.read_until('>',self.timeout)
                tn.write ('set device ' + str(device) + '\r')
                tn.read_until('device',self.timeout)
                tn.read_until('>',self.timeout)

                tn.write ('reboot \r')
                tn.read_until('Rebooting....', self.timeout )
                tn.close()

                self.communicationSuccess(obj)

            except Exception, error:
                self.errorProcessing(obj,error)

        else:
            try:
                tn = telnetlib.Telnet(ip_org,23,self.timeout)

                tn.read_until('>',self.timeout)
                tn.write ('set ip \r')
                tn.read_until('Name:',self.timeout)
                tn.write ( hostname + '\r')
                tn.read_until('Enter:',self.timeout)
                tn.write ('s\r')
                tn.read_until('Address:',self.timeout)
                tn.write ( ip_new + '\r')
                tn.read_until('Mask:',self.timeout)
                tn.write ( subnet + '\r')
                tn.read_until('IP:',self.timeout)
                tn.write ( gateway + '\r')
                tn.read_until('Enter ->',self.timeout)
                tn.write ('y\r')
                tn.read_until('settings.',self.timeout)
                tn.read_until('>',self.timeout)

                tn.write ('set connection\r')
                tn.read_until('Enter:', self.timeout )
                tn.write ('t\r')
                tn.read_until('URL:', self.timeout )
                tn.write ( master + '\r')
                tn.read_until('Port:', self.timeout )
                tn.write ('\r')
                tn.read_until('User:', self.timeout )
                tn.write ('\r')
                tn.read_until('Password:', self.timeout )
                tn.write ('\r')
                tn.read_until('Password:', self.timeout )
                tn.write ('\r')
                tn.read_until('Enter ->', self.timeout )
                tn.write ('y\r')
                tn.read_until('written.',self.timeout)
                tn.read_until('>',self.timeout)
                tn.write ('set device ' + str(device) + '\r')
                tn.read_until('device',self.timeout)
                tn.read_until('>',self.timeout)
                tn.write ('reboot\r')
                tn.read_until('Rebooting....',self.timeout)
                tn.close()

                self.communicationSuccess(obj)

            except Exception, error:
                self.errorProcessing(obj,error)

    def FactoryAV(self, job):

        obj = job[1]
        #command_sent = job[3]
        #port = job[4]


        try:
            tn = telnetlib.Telnet(obj.ip_address,23, self.timeout)

            tn.read_until('>', self.timeout)
            tn.write ('get connection \r')
            tn.read_until('Mode:', self.timeout )
            connection_info = tn.read_very_eager().split()
            #print connection_info
            if connection_info[0] == 'NDP':
                if connection_info[7] == '(n/a)':
                    obj.master = 'not connected'
                    obj.system = 0
                else:
                    obj.master = connection_info[7]
                    obj.system = connection_info[4]

            if connection_info[0] == 'TCP':
                if connection_info[8] == '(n/a)':
                    obj.master = 'not connected'
                    obj.system = 0
                else:
                    obj.master = connection_info[7]
                    obj.system = connection_info[4]


            #command =  command_sent  + "\r"
            command = "send_command " + str(obj.device) + ":" + "1" + ":" + str(obj.system) + " , " + "\"\'FACTORYAV\'\" \r"
            #print command
            tn.write(command)
            tn.read_until('Sending', self.timeout)
            result_raw = tn.read_very_eager()
            result = result_raw.split()
            #print result_raw
            if result[0] != 'command:':
                raise Exception('Command not sent')

            tn.close()

            self.communicationSuccess(obj)

        except Exception, error:
            self.errorProcessing(obj,error)


    def SendCommand(self, job):

        obj = job[1]
        command_sent = job[3]
        port = job[4]


        try:
            tn = telnetlib.Telnet(obj.ip_address,23, self.timeout)

            tn.read_until('>', self.timeout)
            tn.write ('get connection \r')
            tn.read_until('Mode:', self.timeout )
            connection_info = tn.read_very_eager().split()
            #print connection_info
            if connection_info[0] == 'NDP':
                if connection_info[7] == '(n/a)':
                    obj.master = 'not connected'
                    obj.system = 0
                else:
                    obj.master = connection_info[7]

            if connection_info[0] == 'TCP':
                if connection_info[8] == '(n/a)':
                    obj.master = 'not connected'
                    obj.system = 0
                else:
                    obj.master = connection_info[7]


            command =  command_sent  + " \r"
            #print command
            tn.write(str(command))
            tn.read_until('Sending', self.timeout)
            result_raw = tn.read_very_eager()
            result = result_raw.split()
            #print result_raw
            if result[0] != 'command:':
                raise Exception('Command not sent')
            else:
                dispatcher.send( signal="send_command result", sender=('Sending' + str(result_raw[:-1])))


            #if command_sent == 'FACTORYAV':
            #    tn.write ('reboot \r')
            #    tn.read_until('Rebooting....', self.timeout )
            tn.close()

            self.communicationSuccess(obj)

        except Exception, error:
            self.errorProcessing(obj,error)

    def communicationSuccess(self, obj):
        data = [obj.ip_address, 'Success']
        dispatcher.send( signal="Collect Completions", sender=data )

    def errorProcessing(self, obj, error):

        #print(error)
        #print error.args
        error = str(error.args)
        #print error.split()[0] this is what we are matching ... so

        if error.split()[0] == '(113,' or  error.split()[0] == '(111,' or error.split()[0] == "('timed" or error.split()[0] == '(2,':
            data = (obj.ip_address, 'IP unreachable or offline')
        elif error.split()[0] =="('Not,'":
            data = (obj.ip_address, 'Not a DXLink device')
        elif error.split()[0] =="('list":
            data = (obj.ip_address, 'I\'m having trouble communicating with this device')
        elif error.split()[0] == "('Command":
            data = (obj.ip_address, 'Command not sent')
        else:
            data = (obj.ip_address, 'Unable to communicate with device')
        dispatcher.send( signal="Collect Errors", sender=data)


    def SetTurnOnLED(self, job):

        obj = job[1]
        ip = obj.ip_address

        try:
            tn = telnetlib.Telnet(ip,23, self.timeout)
            tn.read_until('>', self.timeout)
            tn.write ('led on \r')
            tn.read_until('ON', self.timeout )
            tn.close()

            self.communicationSuccess(obj)

        except Exception, error:
            self.errorProcessing(obj,error)


    def SetTurnOffLED(self, job):

        obj = job[1]
        ip = obj.ip_address

        try:
            tn = telnetlib.Telnet(ip,23, self.timeout)
            tn.read_until('>', self.timeout)
            tn.write ('led off \r')
            tn.read_until('OFF', self.timeout )
            tn.close()

            self.communicationSuccess(obj)

        except Exception, error:
            self.errorProcessing(obj,error)

    def SetMSE(self, job):

        obj = job[1]
        ip = obj.ip_address
        #print current_thread().getName()
        try:

            tn = telnetlib.Telnet(ip, 23, self.timeout )

            tn.read_until ('Welcome to')

            intro = tn.read_very_eager().split()

            mse = []
            data = []

            while obj.mac_address in self.parent.mse_active_list: # only get if unit is currently being graphed
                #True:
                #print self.parent.mse_active_list
                #for item in self.parent.mse_active_list:
                    #if obj.mac_address == item:
                        #while self.parent.mse_device_listactive:

                tn.write ('show vs100 stats \r')
                stats = tn.read_until('MSE(db)').split()
                #time.sleep(1)

                for i in range(len(stats)):
                	if stats[i] == "ChA:":
                		data.append(stats[i+1][:-1])
                		data.append(stats[i+3][:-1])
                		data.append(stats[i+5][:-1])
                		data.append(stats[i+7])
                #print mse
                if data != []:
                    mse_time = [datetime.datetime.now(),data]
                    #print test
                    mse.append(mse_time)
                    mse.append(obj.ip_address)
                    mse.append(obj.mac_address)

                    dispatcher.send(signal="Incoming MSE", sender=mse)
                    mse = []
                    data = []

        except Exception, error:
            time.sleep(2) # wait for gui to start
            dispatcher.send(signal="MSE error", sender=obj.mac_address)

           
    def SetPing(self, job):
        
        obj = job[1]
        ip = obj.ip_address
        
        #kwargs = {}
        
        #params = dict()
        #startupinfo = subprocess.STARTUPINFO()
        #startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        #params['startupinfo'] = startupinfo

        '''p = subprocess.Popen("cmd.exe", **params)
        if subprocess.mswindows:
             su = subprocess.STARTUPINFO()
             su.dwFlags |= subprocess.STARTF_USESHOWWINDOW
             su.wShowWindow = subprocess.SW_HIDE
             kwargs['startupinfo'] = su 
        #subprocess.Popen("cmd.exe", **kwargs)'''
        ping = subprocess.Popen(['ping' , obj.ip_address , '-t'], shell=True, stdout = subprocess.PIPE)
        #ping = subprocess.Popen("ping %s" % ip, shell=True, 
        #                        stdout=subprocess.PIPE) 
        while self.parent.ping_active:
            for line in iter(ping.stdout.readline,''):
                
                
                result = line.rstrip()
                #print result
                if len(result) < 10:
                    continue
                if result == '':
                    continue
                    #print 'blank'
                    
                elif result == '\n': 
                    continue
                    #print 'next line'
                    
                elif result[:7] == 'Pinging': 
                    continue
                    #print 'pinging'

                elif result.split()[-1] == 'unreachable.' or result == 'Request timed out.':
                    #print result 
                    success = 'No'
                    ms_delay = "N/A"
                    data = (obj,[ datetime.datetime.now(), ms_delay , success])
                    dispatcher.send(signal="Incoming Ping", sender=data)
                    
                elif result.split()[-1][:3] == 'TTL':
                    temp = result.split()[-2]
                    ms_delay = ''.join([str(s) for s in temp if s.isdigit()])
                    success = 'Yes'

                                
                    data = (obj,[ datetime.datetime.now(), ms_delay , success])
                    #print 'sending ping'
                    #print "data: ", data
                    dispatcher.send(signal="Incoming Ping", sender=data)
                    #time.sleep(.5)
                else:
                    #print 'no matches', result
                    success = 'No'
                    ms_delay = "N/A"
                    data = (obj,[ datetime.datetime.now(), ms_delay , success])
                    dispatcher.send(signal="Incoming Ping", sender=data)
                if not self.parent.ping_active: break
            
        ping.kill()