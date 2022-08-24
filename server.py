"""this is the server code for the date-time program --
takes the 3 port numbers as command line arguments """
import socket
import select
import sys
from datetime import datetime


ENG_TO_MAO = {"January": "Kohitātea", "February": "Hui-tanguru",
              "March": "Poutū-te-rangi", "April": "Paenga-whāwhā",
              "May": "Haratua", "June": "Pipiri", "July": "Hōngongoi",
              "August": "Here-turi-kōkā", "September": "Mahuru",
              "October": "Whiringa-ā-nuku", "November": "Whiringa-ā-rangi",
              "December": "Hakihea"}

ENG_TO_GER = {"January": "Januar", "February": "Februar", "March": "März",
              "April": "April", "May": "Mai", "June": "Juni", "July": "Juli",
              "August": "August", "September": "September",
              "October": "Oktober", "November": "November",
              "December": "Dezember"}


class Date_time_server(object):
    """ a date time socket"""

    def __init__(self, port, ptype):
        self.lang = ptype
        self.request_type = 0
        self.port = port
        # sock_dgram for udp
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(('127.0.0.1', port))
        print("{} server running on port: {} ".format(self.lang,
                                                      self. port))

    def get_server(self):
        """returns the server object"""
        return self.server

    def start(self, dt_request_packet: bytearray, address, client):
        """starts processing the request"""
        # process the packet
        is_valid = self.check_packet(dt_request_packet)
        if not is_valid:
            # packet is not valid: discard packet
            print("discarding packet")
            return

        # check request type and create response packet
        self.request_type = (dt_request_packet[4] << 8) | dt_request_packet[5]
        response_packet = self.create_response_packet()
        # send packet back to client
        client.sendto(response_packet, address)

    def check_packet(self, packet: bytearray) -> bool:
        """checks that the packet is valid, does not check the
        request type """
        # check the magicNo
        magic_n = (packet[0] << 8) | packet[1]
        if magic_n != 0x497E:
            print("ERROR: the magic number is incorrrect")
            return False
        # check the packetype
        packet_type = (packet[2] << 8) | packet[3]
        if packet_type != 1:
            print("ERROR: the packet type is incorrect")
            return False
        return True

    def create_response_packet(self) -> bytearray:
        """creates a response packet to send to the client"""
        # construct text
        text = self.construct_date_time()
        text = text.encode("utf-8")
        text_length = len(text)

        packet = bytearray(13)
        # create magic number
        magic_number = 0x497E
        packet[0] = magic_number >> 8
        packet[1] = magic_number & 0xFF
        # create packet type
        packet_type = 0x0002
        packet[2] = packet_type >> 8
        packet[3] = packet_type & 0xFF
        # use the langage code
        if self.lang == 'eng':
            language_code = 0x0001
        elif self.lang == 'mao':
            language_code = 0x0002
        elif self.lang == 'ger':
            language_code = 0x0003

        packet[4] = language_code >> 8
        packet[5] = language_code & 0xFF

        # date time
        now = datetime.now()
        curr_year = int(now.strftime("%Y"))
        curr_month = int(now.strftime("%m"))
        curr_day = int(now.strftime("%d"))
        curr_hour = int(now.strftime("%H"))
        curr_minute = int(now.strftime("%M"))

        # year
        packet[6] = curr_year >> 8
        packet[7] = curr_year & 0xFF
        # month: all fields from here are 1 byte
        packet[8] = curr_month
        # day
        packet[9] = curr_day
        # hour
        packet[10] = curr_hour
        # minute
        packet[11] = curr_minute
        # next field is the length field
        packet[12] = text_length + 13
        # text added to bytearray
        packet = packet + text
        return packet

    def construct_date_time(self) -> str:
        """constructs the english string """
        date_time = datetime.now()

        if self.request_type == 0x001:

            date = date_time.strftime("%d, %Y")
            month = date_time.strftime("%B")

            if self.lang == "eng":
                lang_string = "Todays date is"

            elif self.lang == "mao":
                lang_string = "Ko te ra o tenei ra ko"
                month = ENG_TO_MAO[month]

            elif self.lang == "ger":
                lang_string = "Heute ist der"
                month = ENG_TO_GER[month]

            return f"{lang_string} {month}, {date}"

        elif self.request_type == 0x0002:

            time = date_time.strftime("%H:%M")
            if self.lang == "eng":
                time_string = "The current time is"
            elif self.lang == "mao":
                time_string = "Ko te wa o tenei wa"
            elif self.lang == "ger":
                time_string = "Die Uhrzeit ist"

            return time_string + time


def set_ports() -> tuple[int, int, int]:
    """queries the user for the port numbers"""
    try:
        eng_port, mao_port, ger_port = sys.argv[1:5]
    except ValueError:
        print("ERROR: Incorrect number of arguments")
        quit()
    # check that the ports are a valid number
    is_valid_port(eng_port, 'English port')
    is_valid_port(mao_port, 'Maori port')
    is_valid_port(ger_port, 'German port')

    return eng_port, mao_port, ger_port


def is_valid_port(port, name):
    """prints an error message and quits the program if the port is invalid"""
    if (int(port) < 1024 or int(port) > 64000):
        print(f"ERROR: {name} is an invalid port number")
        quit()


def main():
    """the main function for the server, uses threading to use multiple
    sockets"""
    eng_port, mao_port, ger_port = set_ports()

    eng_server = Date_time_server(int(eng_port), "eng")
    mao_server = Date_time_server(int(mao_port), "mao")
    ger_server = Date_time_server(int(ger_port), "ger")

    sockets = [eng_server.get_server(), mao_server.get_server(),
               ger_server.get_server()]

    while True:
        inputready, outputready, exceptready = select.select(sockets, [], [])

        for client in inputready:

            dt_request_packet, address = client.recvfrom(1024)

            # check the port that was used
            if client.getsockname()[1] == int(eng_port):
                eng_server.start(dt_request_packet, address, client)
            elif client.getsockname()[1] == int(mao_port):
                mao_server.start(dt_request_packet, address, client)
            elif client.getsockname()[1] == int(ger_port):
                ger_server.start(dt_request_packet, address, client)
            else:
                print("ERROR: port not recognised")


main()
