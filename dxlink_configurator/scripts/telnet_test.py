#telnet_test.py

import telnetlib
import time


def call_back(sock, cmd, opt):
    #print sock, opt
    # This is supposed to turn server side echoing on and turn other options off.
    if opt == telnetlib.ECHO and cmd in (telnetlib.WILL, telnetlib.WONT):
        #print 'echo'
        sock.sendall(telnetlib.IAC + telnetlib.DO + telnetlib.ECHO)
        #time.sleep(2)
#    elif opt != telnetlib.NOOPT:
#        if cmd in (telnetlib.DO, telnetlib.DONT):
#            print 'i dont know'
#            sock.sendall(telnetlib.IAC + telnetlib.WONT + opt)
##        elif cmd in (telnetlib.WILL, telnetlib.WONT):
#            print 'still dont know'
#            #if opt == telnetlib.
#            sock.sendall(telnetlib.IAC + telnetlib.DONT + opt)

def set_option(socket, command, option):
    """ Configure our telnet options. This is magic. Don't touch it. """

    if command == telnetlib.DO and option == "\x18":
        print 'terminal'
        # Promise we'll send a terminal type
        socket.send("%s%s\x18" % (telnetlib.IAC, telnetlib.WILL))
    elif command == telnetlib.DO and option == "\x01":
        print 'echo'
        # Pinky swear we'll echo
        socket.send("%s%s\x01" % (telnetlib.IAC, telnetlib.WILL))
    elif command == telnetlib.DO and option == "\x1f":
        print 'window'
        # And we should probably tell the server we will send our window
        # size
        socket.send("%s%s\x1f" % (telnetlib.IAC, telnetlib.WILL))
    elif command == telnetlib.DO and option == "\x20":
        print 'speed'
        # Tell the server to sod off, we won't send the terminal speed
        socket.send("%s%s\x20" % (telnetlib.IAC, telnetlib.WONT))
    elif command == telnetlib.DO and option == "\x23":
        print 'x-display'
        # Tell the server to sod off, we won't send an x-display terminal
        socket.send("%s%s\x23" % (telnetlib.IAC, telnetlib.WONT))
    elif command == telnetlib.DO and option == "\x27":
        print 'environment'
        # We will send the environment, though, since it might have nethack
        # specific options in it.
        socket.send("%s%s\x27" % (telnetlib.IAC, telnetlib.WILL))
    '''elif self.conn.rawq.startswith("\xff\xfa\x27\x01\xff\xf0\xff\xfa"):
        # We're being asked for the environment settings that we promised
        # earlier
        socket.send("%s%s\x27\x00%s%s%s" %
                    (telnetlib.IAC,
                     telnetlib.SB,
                     '\x00"NETHACKOPTIONS"\x01"%s"' % os.environ.get("NETHACKOPTIONS", ""),
                     telnetlib.IAC,
                     telnetlib.SE))
        # We're being asked for the terminal type that we promised earlier
        socket.send("%s%s\x18\x00%s%s%s" % 
                    (telnetlib.IAC,
                     telnetlib.SB,
                     "xterm-color",
                     telnetlib.IAC,
                     telnetlib.SE))'''

tn = telnetlib.Telnet('192.168.7.176', 23) # DXLink
#tn = telnetlib.Telnet('192.168.0.3', 23) # DVX
#tn = telnetlib.Telnet('192.168.7.174', 15000) # DGX
#tn.set_debuglevel(100)
#tn.read_sb_data()

#ime.sleep(5)
tn.set_option_negotiation_callback(call_back)
test_list = ([
    'AO', 'AUTHENTICATION', 'AYT', 'BINARY', 'BM', 'BRK', 'CHARSET', 
    'COM_PORT_OPTION', 'DEBUGLEVEL', 'DET', 'DM', 'DO', 'DONT', 'EC', 'ECHO', 
    'EL', 'ENCRYPT', 'EOR', 'EXOPL', 'FORWARD_X', 'GA', 'IAC', 'IP', 'KERMIT', 
    'LFLOW', 'LINEMODE', 'LOGOUT', 'NAMS', 'NAOCRD', 'NAOFFD', 'NAOHTD', 
    'NAOHTS', 'NAOL', 'NAOLFD', 'NAOP', 'NAOVTD', 'NAOVTS', 'NAWS', 
    'NEW_ENVIRON', 'NOOPT', 'NOP', 'OLD_ENVIRON', 'OUTMRK', 'PRAGMA_HEARTBEAT', 
    'PRAGMA_LOGON', 'RCP', 'RCTE', 'RSP', 'SB', 'SE', 'SEND_URL', 'SGA', 
    'SNDLOC', 'SSPI_LOGON', 'STATUS', 'SUPDUP', 'SUPDUPOUTPUT', 
    'SUPPRESS_LOCAL_ECHO', 'TELNET_PORT', 'TLS', 'TM', 'TN3270E', 'TSPEED', 
    'TTYLOC', 'TTYPE', 'TUID', 'VT3270REGIME', 'WILL', 'WONT', 'X3PAD', 
    'XASCII', 'XAUTH', 'XDISPLOC'])

#for item in test_list:
#    print item, getattr(telnetlib, item)
##print telnetlib.ECHO
#print telnetlib.NOOPT
#print dir(telnetlib)

'''
####DGX stuff#####
print tn.read_until('successful')
#time.sleep(2)
tn.write('\x03')
tn.read_until('SHELL>')
tn.write('show' + '\r\n')
time.sleep(2)
print tn.read_until('SHELL>')
tn.close() '''

####DXLink####
'''
print tn.read_until('Welcome')
print tn.read_until('>')

tn.write('get ip\r\n')
#time.sleep(2)
print tn.read_until('>')

tn.write('get ip\r\n')
#time.sleep(2)
print tn.read_until('>')'''
'''
tn.write('?\r\n')
#time.sleep(2)
print tn.read_until('show tcp')
print tn.read_until('>')'''

### NI ####
'''
print tn.read_until('Welcome')
print tn.read_until('>')

tn.write('get ip\r\n')
#time.sleep(2)
print tn.read_until('>')

tn.write('?\r\n')
#time.sleep(2)
print tn.read_until('show tcp')
print tn.read_until('>')'''


#test = tn.read_until('>', 5)
#if test == '':
#    print 'test = ', test
#else:
#    print test
#print tn.read_until('>', 5)



#tn = telnetlib.Telnet(obj.ip_address, 23, 5)
            
tn.read_until('Welcome to', 5)
intro = tn.read_until('>').split()
model = intro[0]
firmware = intro[1]

tn.write('get sn \r')
tn.read_until('Number:', 5)
serial = tn.read_until('>').split()[0]

tn.write('get device \r')
tn.read_until('Value:', 5)

device = tn.read_until('>').split()[0]

tn.write('get ip \r')
tn.read_until('HostName:', 5)
ip_host = tn.read_until('Type:').split()
if len(ip_host) == 1:
    hostname = ''
else:
    hostname = ' '.join(ip_host[:-1])
ip_type = tn.read_until('IP').split()

if ip_type[0] == "Static":
    ip_type = "s"
if ip_type[0] == "DHCP":
    ip_type = "d"
ip_subnet = tn.read_until('Gateway').split()
subnet = ip_subnet[-2]
ip_gateway = tn.read_until('MAC').split()
gateway = ip_gateway[-2]
ip_mac = tn.read_until('>').split()
mac_address = ip_mac[1]
#self.get_connection(obj, tn, 5)

print 'intro', intro
print 'model', model
print 'firmware', firmware
print 'serial', serial
print 'device', device
print 'ip_host', ip_host
print 'hostname', hostname
print 'ip_type', ip_type
print 'ip_subnet', ip_subnet
print 'ip_gateway', ip_gateway
print 'mac_address', mac_address

tn.write('exit')























tn.close()




