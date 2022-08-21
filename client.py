import socket

BUFSIZE = 6  # size of the packet that will be recieved from server


class Date_time_client(object):
    """the class for the date time client"""

    def __init__(self, port=6969, host=socket.gethostbyname(
                                    socket.gethostname()), req_type='date'):
        self.request_type = req_type
        self.ADDR = (host, port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.connect(self.ADDR)

    def send_request(self):
        """sends a request to the server"""
        request_packet = self.create_request_packet()
        self.client.send(request_packet)


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


def get_request_type() -> str:
    """this will see if the user wants to recieve the date or time"""

    print("Do you wish to recieve the date or time?")
    req_type = input("")
    if req_type.lower() != "time" and req_type.lower() != "date":
        print("ERROR: Invalid request type")
        print("exiting server...")
        quit()
    else:
        return req_type


def get_ip_addr() -> str:
    """queries the user for the ip address and checks if it is valid"""

    pass


def get_port_num() -> int:
    """queries the user for the port numebr and checks if its valid"""

    print("please enter the port number")
    port = input("")
    port = int(port)

    if port < 1024 or port > 64000:
        print("ERROR: port must be in the range 1024-64000")
        print("exiting server...")
        quit()
    else:
        return port


def main():
    """the main function for the client"""

    # req_type = get_request_type()
    ip_addr = get_ip_addr()
    port_num = get_port_num()
    client = Date_time_client()
    client.send_request()


main()
