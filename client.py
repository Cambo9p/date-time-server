import socket


BUFSIZE = 6  # size of the packet that will be recieved from server


class Date_time_client(object):
    """the class for the date time client"""

    def __init__(self, port=6969, host = socket.gethostbyname(
                                    socket.gethostname())):
        self.ADDR = (host, port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.connect(self.ADDR)

    def send_request(self):
        """sends a request to the server"""
        msg = "hello"
        message = msg.encode('utf-8')
        msg_length = len(message)
        send_length = str(msg_length).encode('utf-8')
        # find the paddding
        self.client.send(send_length)
        self.client.send(message)


client = Date_time_client()
client.send_request()
