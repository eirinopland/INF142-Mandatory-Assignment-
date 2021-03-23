from socket import socket

sock = socket()

sock.connect(("localhost", 55555))

while (text := input("> ").lower()) != "shut down":
    sock.sendto(text.encode(), ("localhost", 55555))

