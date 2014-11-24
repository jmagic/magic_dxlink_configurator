#telnet_test.py

import telnetlib
import time


def call_back(sock, cmd, opt):
    #print sock, opt
    # This is supposed to turn server side echoing on and turn other options off.
    if opt == telnetlib.ECHO and cmd in (telnetlib.WILL, telnetlib.WONT):
        #print 'echo'
        sock.sendall(telnetlib.IAC + telnetlib.DO + telnetlib.ECHO)
    elif opt != telnetlib.NOOPT:
        if cmd in (telnetlib.DO, telnetlib.DONT):
            print 'i dont know'
            sock.sendall(telnetlib.IAC + telnetlib.WONT + opt)
        elif cmd in (telnetlib.WILL, telnetlib.WONT):
            print 'still dont know'
            sock.sendall(telnetlib.IAC + telnetlib.DONT + opt)

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

tn = telnetlib.Telnet('10.0.0.1', 23)
#ime.sleep(5)
tn.set_option_negotiation_callback(call_back)

print tn.read_until('Welcome')
print tn.read_until('>')

tn.write('get ip\r\n')
#time.sleep(2)
print tn.read_until('>')

tn.write('?\r\n')
#time.sleep(2)
print tn.read_until('show tcp')
print tn.read_until('>')
test = tn.read_until('>', 5)
if test == '':
    print 'test = ', test
else:
    print test
#print tn.read_until('>', 5)
tn.close()




