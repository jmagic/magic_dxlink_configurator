
import telnetlib

def set_option(socket, command, option):
        """ Configure our telnet options. This is magic. Don't touch it. """

        if command == telnetlib.DO and option == "\x18":
            print 'x18'
            # Promise we'll send a terminal type
            socket.send("%s%s\x18" % (telnetlib.IAC, telnetlib.WILL))
        elif command == telnetlib.DO and option == "\x01":
            print 'x01'
            # Pinky swear we'll echo
            socket.send("%s%s\x01" % (telnetlib.IAC, telnetlib.WILL))
        elif command == telnetlib.DO and option == "\x1f":
            print 'x1f'
            # And we should probably tell the server we will send our window
            # size
            socket.send("%s%s\x1f" % (telnetlib.IAC, telnetlib.WILL))
        elif command == telnetlib.DO and option == "\x20":
            print 'x20'
            # Tell the server to sod off, we won't send the terminal speed
            socket.send("%s%s\x20" % (telnetlib.IAC, telnetlib.WONT))
        elif command == telnetlib.DO and option == "\x23":
            print 'x23'
            # Tell the server to sod off, we won't send an x-display terminal
            socket.send("%s%s\x23" % (telnetlib.IAC, telnetlib.WONT))
        elif command == telnetlib.DO and option == "\x27":
            print 'x27'
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


tn = telnetlib.Telnet('192.168.7.176', 23)
tn.set_option_negotiation_callback(set_option)


print tn.read_until('Welcome')
print tn.read_very_eager()
tn.write('\r\n')
print tn.read_very_eager()
tn.write('\r\n')
print tn.read_very_eager()
tn.close()


