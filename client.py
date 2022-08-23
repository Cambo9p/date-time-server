import socket
import sys
import select

BUFSIZE = 6  # size of the packet that will be recieved from server


class Date_time_client(object):
    """the class for the date time client"""

    def __init__(self, port, host_ip, req_type='date'):
        self.request_type = str(req_type)
        self.port = port
        self.ip_addr = host_ip
        self.ADDR = (host_ip, int(port))
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.connect(self.ADDR)

    def recieve_response(self):
        """the client will wait to recieve a responce from the server"""

        inputs = [self.client]
        self.outputs = []

        try:
            inputready, outputready, exceptready = select.select(inputs,
                                                                 self.outputs,
                                                                 [], 10)
            message = inputready[0].recv(1024)
            print("message recieved: ", message)

        except IndexError:
            print("ERROR: more than one second to recieve response")

    def send_request(self):
        """sends a request to the server"""
        request_packet = self.create_request_packet()
        # self.client.send(request_packet)
        print('REQUEST PACKET ', request_packet, 'ADDR ', (str(self.ip_addr),
                                                           int(self.port)))
        self.client.sendto(request_packet, (str(self.ip_addr), int(self.port)))
        # self.client.close()

    def create_request_packet(self) -> bytearray:
        """Creates the dt-request packet to send to the server"""

        request = bytearray(6)  # creates a bytearray of size 6
        # first two bytes are the magic number
        magic_num = 0x497E
        request[0] = magic_num >> 8
        request[1] = magic_num & 0xFF
        # second two bytes are the packet type
        packet_type = 0x0001
        request[2] = packet_type >> 8
        request[3] = packet_type & 0xFF
        # third two bytes are the request type
        if self.request_type == 'date':
            request_num = 0x0001
        else:
            request_num = 0x0002
        request[4] = request_num >> 8
        request[5] = request_num & 0xFF

        return request


def return_args():
    """returns the command line argument - request_type, ip, port"""

    try:
        request_type, ipaddress, port_number = sys.argv[1:5]
    except ValueError:
        print("ERROR: too many arguments given")

    # check that the values are correct
    check_request(request_type)
    ip_addr = check_ip_addr(ipaddress)
    check_port(port_number)

    return request_type, ip_addr, port_number


def check_ip_addr(ip_addr) -> str:
    """checks to see if the ip address is valid """
    try:
        ip = socket.gethostbyname(ip_addr)
    except socket.gaierror:
        # ip address is not legal
        print("ERROR: invalid IP address")
        quit()
    return ip


def check_port(port) -> None:
    """checks to see if the port number is correct"""
    if int(port) < 1024 or int(port) > 64000:
        print("ERROR: invalid port number")
        quit()


def check_request(request_type) -> None:
    """checks that the request type is valid"""
    if str(request_type) != "date" and request_type != "time":
        print("ERROR: invalid request type '{}'".format(request_type))
        quit()


def main():
    """the main function for the client"""

    request_type, ip_addr, port_number = return_args()
    client = Date_time_client(port_number, ip_addr, request_type)
    client.send_request()
    client.recieve_response()


main()
