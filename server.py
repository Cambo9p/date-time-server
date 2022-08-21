"""this is the server code for the date-time program - see README.md for
details"""

import socket
import select
import sys

BUFSIZE = 6  # size of the packet that will be recieved from client


class Date_time_server(object):
    """ a date time server using select"""

    def __init__(self, port=6969, ptype='eng'):
        self.lang = ptype
        # sock_dgram for udp
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(('', port))

    def start(self):
        """starts searching for connections """

        inputs = [self.server, sys.stdin]
        self.outputs = []
        running = True

        while running:

            try:
                inputready, outputready, exceptready = select.select(
                    inputs, self.outputs, [])

            except select.error as e:
                print(e)
                break
            except socket.error as e:
                print(e)
                break

            for s in inputready:

                message = s.recv(BUFSIZE)  # message is correct size
                print(bytearray(message).hex())


def set_ports() -> tuple[int, int, int]:
    """queries the user for the port numbers"""

    print("please enter the English port")
    eng_port = input('')
    is_valid_port(eng_port, 'English port')

    print("please enter the Maori port")
    mao_port = input('')
    is_valid_port(mao_port, 'Maori port')

    print("please enter the German port")
    ger_port = input('')
    is_valid_port(ger_port, 'German port')

    return eng_port, mao_port, ger_port


def is_valid_port(port, name):
    """prints an error message and quits the program if the port is invalid"""
    if (int(port) < 1024 or int(port) > 64000):
        print(f"ERROR: {name} is an invalid port number")
        quit()


if __name__ == "__main__":

    eng_port, mao_port, ger_port = set_ports()
    Date_time_server(int(eng_port)).start()
