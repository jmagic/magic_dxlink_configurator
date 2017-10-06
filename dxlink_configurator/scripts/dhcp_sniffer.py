"""A DCHP sniffer that listens for DHCP request messages"""
import socket
import time
from threading import Thread
from pydispatch import dispatcher


class DHCPListener(Thread):
    """The dhcp listener thread"""

    def __init__(self):
        """Init Worker Thread Class."""
        self.shutdown = False
        Thread.__init__(self)

    def run(self):
        """Run Worker Thread."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            port = 67
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("", port))
            sock.setblocking(0)

        except IOError:
            # something has already used the port, its probably not us because
            # multiple instances can run without error due to SO_REUSEADDR
            dispatcher.send(signal="DHCPListener", sender=self, data={'Error': 'Socket in use'})

        while not self.shutdown:
            try:
                msg, _ = sock.recvfrom(1024)
            except Exception as error:
                if error.args[0] == 10035:
                    # no data
                    # lets wait a bit and check again
                    time.sleep(1)
                    continue
                else:
                    print("Error listening: ", error)
            # check if it is a DHCP "request" message
            try:
                # print(".".join([str(item) for item in msg[240:243]]))
                # print(msg[240:243] == b'\x35\x01\x03')
                if msg[240:243] == b'\x35\x01\x03':
                    # extract the sending mac address
                    mac_address = ':'.join(['%02x' % item for item in msg[28:34]])

                    # process only the DHCP options portion of the packet
                    dhcp_options = msg[243:]
                    ip_address = ''
                    hostname = ''
                    # print(repr(dhcp_options))
                    # print('going into options')
                    while dhcp_options:
                        opt = dhcp_options[0]

                        if opt == 255:  # end of packet
                            # print('found end')
                            break

                        if opt == 0:  # padding in packet
                            dhcp_options = dhcp_options[1:]  # move to the next byte
                            # print('found padding')
                            continue

                        if opt == 50:  # requested IP
                            # print('found IP')
                            # We need to move to the data,
                            # and read the length of it
                            # convert what we got from hex to decimal and put into
                            # string with dots
                            data, dhcp_options = self.get_data(dhcp_options)
                            # length = dhcp_options[1]
                            # # Remove opt and length
                            # dhcp_options = dhcp_options[2:]
                            ip_address = '.'.join([str(item) for item in data])
                            # Remove ip
                            # dhcp_options = dhcp_options[length:]
                            continue

                        # hostname
                        if opt == 12:
                            # print('found hostname')
                            # convert what we got to a string
                            data, dhcp_options = self.get_data(dhcp_options)
                            # length = dhcp_options[1]
                            # dhcp_options = dhcp_options[2:]

                            hostname = ''.join([chr(item) for item in data])
                            # dhcp_options = dhcp_options[length:]
                            continue

                        # Unknown option -- skip it
                        data, dhcp_options = self.get_data(dhcp_options)
                        # length = dhcp_options[1]
                        # # Remove opt and length
                        # dhcp_options = dhcp_options[2:]
                        # print("data: ", repr(data))
                        # dhcp_options = dhcp_options[length:]

                    if ip_address == '':
                        print('no ip skipping')
                        continue

                    # check if we have been told to stop listening
                    if not self.shutdown:
                        dispatcher.send(signal="Incoming Packet", sender=(hostname, mac_address, ip_address))
            except Exception as error:
                print('Error parsing DHCP packet: ', error)

    def get_data(self, dhcp_options):
        """Gets variable length data, and returns data and left over options"""
        length = dhcp_options[1]
        data = dhcp_options[2:length + 2]
        dhcp_options = dhcp_options[length + 2:]
        return data, dhcp_options


def incoming(sender):
    print(sender)


def main():
    dispatcher.connect(incoming, signal="Incoming Packet", sender=dispatcher.Any)
    test = DHCPListener()
    test.start()
    import time
    time.sleep(20)
    test.shutdown = True
    test.join()

if __name__ == '__main__':
    main()

