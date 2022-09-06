# date-time-server
This is a Clinet/Server command line application run over UDP that will send the date or time in a specific language to the client 

Run the server on the terminal using "python3 server.py port1 port2 port3" where ports 1,2 and 3 are the port numbers for an english date/time, a maori date/time and a german date/time respectively.

to run the client on the terminal run "pyhon3 client.py req ip port" where req is either date or time, ip is the ip address of the machine and port is the port running the server.
