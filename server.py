from socket import socket, AF_INET, SOCK_DGRAM

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(("localhost", 55555))

"""
The while loop functions as a "block".
The code will not continue until information is received 
in line 12 and added to the variable names.
"""
while True:
    msg, addr = sock.recvfrom(2048)
    print(f"{addr[0]} says {msg.decode()}")