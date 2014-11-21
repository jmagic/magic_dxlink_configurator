"""A DCHP sniffer that listens for DHCP request messages"""

from threading import Thread
import socket
from pydispatch import dispatcher
import wx

########################################################################
class DHCPListener(Thread):
    """The dhcp listener thread"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Init Worker Thread Class."""
        self.listen = True
        self.parent = parent
        self.lis_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dhcp_options = None
        self.dhcp_sniffing_enabled = False
        self.shutdown = False
        
        Thread.__init__(self)

    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""

        try:
            port = 67
            self.lis_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.lis_sock.bind(("", port))

        except IOError:
            # something has already used the port, its probably not us because
            # multiple instances can run without error due to SO_REUSEADDR
            self.parent.portError = True

        
        
        
        while not self.shutdown:
            msg, _ = self.lis_sock.recvfrom(1024)
            # check if it is a DHCP "request" message
            if ((msg[240] == "\x35" and 
                 msg[241] == "\x01" and 
                 msg[242] == "\x03")):

                # extract the sending mac address
                mac_address = (
                    msg[28].encode("hex") + ":" +
                    msg[29].encode("hex") + ":" +
                    msg[30].encode("hex") + ":" +
                    msg[31].encode("hex") + ":" +
                    msg[32].encode("hex") + ":" +
                    msg[33].encode("hex")
                    )

                #process only the DHCP options portion of the packet
                self.dhcp_options = msg[243:]
                ip_address = ''
                hostname = ''

                while self.dhcp_options:

                    opt = self.dhcp_options[0]

                    #end of packet
                    if opt == '\xff':
                        self.dump_byte() #move to the next byte
                        break

                    # padding in packet
                    if opt == '\x00':
                        self.dump_byte() #move to the next byte
                        continue

                    # requested IP
                    if opt == '\x32':
                        # We need to move to the data, and read the length of it
                        # convert what we got from hex to decimal and put into 
                        # string with dots
                        ip_address = '.'.join(
                            str(ord(c)) for c in 
                            (self.read_data(self.get_to_data())))
                        continue

                    # hostname
                    if opt == '\x0c':
                        # convert what we got to a string
                        hostname = ''.join((c) for c in (
                            self.read_data(self.get_to_data())))
                        continue

                    self.read_data(self.get_to_data())


                if ip_address == '':
                    continue

                # check if we have been told to stop listening
                if not self.shutdown and self.dhcp_sniffing_enabled:
                    #send the processed packet to the main loop
                    wx.CallAfter(
                        self.send_info, (hostname, mac_address, ip_address))



    def read_data(self, data_length):
        """Reads the data portion of the DHCP option"""
        read_data = []
        for _ in range(0, data_length):
            read_data.append(self.dhcp_options[0])
            self.dhcp_options = self.dhcp_options[1:]
        return read_data


    def dump_byte(self):
        """Move to the next byte"""
        self.dhcp_options = self.dhcp_options[1:] #move one byte


    def get_to_data(self):
        """Read the data length and option number then move to the data"""
        self.dump_byte() # move to data length
        data_length = ord(self.dhcp_options[0]) # get data length
        self.dump_byte() #move to start of data
        return data_length

    #----------------------------------------------------------------------
    def send_info(self, info):
        """
        Send data to GUI
        """
        #print 'got info', info
        dispatcher.send(signal="Incoming Packet", sender=info)

########################################################################

