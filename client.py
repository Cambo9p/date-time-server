import socket
import sys
import select


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
            # final param means the client will wait 1 second for a response
            inputready, outputready, exceptready = select.select(inputs,
                                                                 self.outputs,
                                                                 [], 1)
            response_packet = inputready[0].recv(1024)

        except IndexError:
            print("ERROR: more than one second to recieve response")
            quit()
        # check the response_packet
        self.check_response(response_packet)
        # print the contents of the dt response packet
        self.print_response(response_packet)

    def print_response(self, packet: bytearray) -> None:
        """prints the fields in the dt_response_packet"""
        print("Magic numeber: ", (packet[0] << 8) | packet[1])
        print("packet type: ", (packet[2] << 8) | packet[3])
        print("language code: ", (packet[4] << 8) | packet[5])
        print("year: ", (packet[6] << 8) | packet[7])
        print("month: ", packet[8])
        print("day: ", packet[9])
        print("hour: ", packet[10])
        print("minute: ", packet[11])
        print("length: ", packet[12])
        print("text: ", packet[13:].decode())
        quit()

    def check_response(self, packet: bytearray) -> None:
        """checks if the dt response packet is valid"""
        # check that the packet has at least 13 bytes of data
        if len(packet) < 13:
            print("ERROR: not all header fields present")
            quit()
        # check the magic number
        magic_num = (packet[0] << 8) | packet[1]
        if magic_num != 0x497E:
            print("ERROR: incorrect magic num '{}'".format(magic_num))
            quit()
        # check the packet type
        packet_type = (packet[2] << 8) | packet[3]
        if packet_type != 0x0002:
            print("ERROR: incorrect packet type '{}'".format(packet_type))
            quit()
        # check the language code
        language_code = (packet[4] << 8) | packet[5]
        if (language_code != 0x0001 and language_code != 0x0002 and
                language_code != 0x0003):
            print("ERROR: invalid language code '{}'".format(language_code))
            quit()
        # check the year
        year = (packet[6] << 8) | packet[7]
        if year >= 2100:
            print("ERROR: invlaid year '{}'".format(year))
            quit()
        # check month
        month = (packet[8])
        if month < 1 or month > 12:
            print("ERROR: invalid month '{}'".format(month))
            quit()
        # check day
        day = packet[9]
        if day < 1 or day > 32:
            print("ERROR: invalid day '{}'".format(day))
            quit()
        # check hour
        hour = packet[10]
        if hour < 0 or hour > 23:
            print("ERROR: invalid hour '{}'".format(day))
            quit()
        # check minute
        minute = packet[11]
        if minute < 0 or minute > 59:
            print("ERROR: invalid minute '{}'".format(minute))
            quit()
        # check length
        length = packet[12]
        if length != 13 + len(packet[13:]):
            print("ERROR: incorrect length '{}'".format(length))
            quit()
        # all checks passed

    def send_request(self):
        """sends a request to the server"""
        request_packet = self.create_request_packet()
        self.client.sendto(request_packet, (str(self.ip_addr), int(self.port)))

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
