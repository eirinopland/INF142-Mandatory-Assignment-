from socket import socket

sock = socket()

sock.connect(("localhost", 5555))

while (text := input("> ").lower()) != "shut down":
    sock.sendto(text.encode(), ("localhost", 5555))
