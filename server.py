"""this is the server code for the date-time program - see README.md for
details"""

import socket
import select
import sys

BUFSIZE = 6 # size of the packet that will be recieved from client

class Date_time_server(object):
    """ a date time server using select"""

    def __init__(self, port= 6969):
        self.clients = 0
        # sock_dgram for udp
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(('',port))

    def start(self):
        """starts searching for connections """

        inputs = [self.server,sys.stdin]
        self.outputs = []
        running = True

        while running:

            try:
                inputready,outputready,exceptready = select.select(inputs,
                                                                   self.outputs,
                                                                   [])
            except select.error as e:
                break
            except socket.error as e:
                break


            for s in inputready:

                message = s.recv(BUFSIZE) # message is correct size
                print(message)


if __name__ == "__main__":
    Date_time_server().start()
