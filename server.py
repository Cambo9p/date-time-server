"""this is the server code for the date-time program - see README.md for
details"""
# TODO: create unit tests
# TODO: change date string to utf-8 and put the text_length field into the
# bytearray
import socket
import select
import sys
import datetime


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

            for client in inputready:

                message = bytearray(client.recv(BUFSIZE))
                print((message).hex())
                # process the packet
                is_valid = self.check_packet(message)
                if not is_valid:
                    # packet is not valid: discard packet
                    print("discarding packet")
                    continue
                # packet is valid
                # check request type and create response packet
                request_type = (message[4] << 0xFF) & message[5]
                if request_type == 0x0001:
                    # date
                    pass
                elif request_type == 0x0002:
                    # time
                    pass
                else:
                    print("incorrect request type")
                    print("discarding packet")
                    continue

    def check_packet(self, packet: bytearray) -> bool:
        """checks that the packet is valid, does not check the
        request type """
        # check the magicNo
        magic_n = (packet[0] << 0xFF) & packet[1]
        if magic_n != 0x497E:
            print("ERROR: the magic number is incorrrect")
            return False
        # check the packetype
        packet_type = (packet[2] << 0xFF) & packet[3]
        if packet_type != 1:
            print("ERROR: the packet type is incorrect")
            return False
        return True

    def create_response_packet(self) -> bytearray:
        """creates a response packet to send to the client"""
        packet = bytearray(13)
        # create magic number
        magic_number = 0x497E
        packet[0] = magic_number >> 8
        packet[1] = magic_number & 0xFF
        # create packet type
        packet_type = 0x0002
        packet[2] = packet_type >> 8
        packet[3] = packet_type & 0xFF

        if self.lang == 'eng':
            language_code = 0x0001
        elif self.lang == 'mao':
            language_code = 0x0002
        elif self.lang == 'ger':
            language_code = 0x0003

        packet[4] = language_code >> 8
        packet[5] = language_code & 0xFF

        # date time
        date_time = datetime.datetime.now()
        curr_year = date_time.date.strftime("%Y")
        curr_month = date_time.date.strftime("%m")
        curr_day = date_time.date.strftime("%d")
        curr_hour = date_time.date.strftime("%H")

        # year
        packet[6] = curr_year >> 8
        packet[7] = curr_year & 0xFF
        # month is 1 byte
        packet[8] = curr_month
        # day
        packet[9] = curr_day
        # hour
        packet[10] = curr_hour
        # next field is the length field
        # construct the text
        if self.lang == 'eng':
            pass

    def construct_date_time(self, type_flag: str) -> str:
        """constructs the english string """
        date_time = datetime.datetime.now()

        if type_flag == "date":

            date = date_time.date.strftime("%d, %Y")
            month = date_time.date.strftime("%B")

            if self.lang == "eng":
                lang_string = "Todays date is "

            elif self.lang == "mao":
                lang_string = "Ko te ra o tenei ra ko "
                month = ENG_TO_MAO[month]

            elif self.lang == "ger":
                lang_string = "Heute ist der "
                month = ENG_TO_GER[month]

            return f"{lang_string} {month}, {date}"

        elif type_flag == "time":

            time = date_time.date.strftime("%H:%M")
            if self.lang == "eng":
                time_string = "The current time is "
            elif self.lang == "mao":
                time_string = "Ko te wa o tenei wa "
            elif self.lang == "ger":
                time_string = "Die Uhrzeit ist "

            return time_string + time


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
