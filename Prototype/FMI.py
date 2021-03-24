from socket import socket


class FMI:
    def __init__(self, server):
        self.server = server

    def retrieve_data_from_server(self, server, location):
        sock = socket()
        sock.connect(server)
        sock.send(location.encode())
        data = sock.recv(1024).decode()

        print(f"From storage {server.server_id}:\nTemperature\tPrecipitation\n {data}")  #
        sock.close()

    def input_from_cli(self,):
        location = input("Choose weather station (1,2,3): ")
        server_num = 0

        # change this:
        if location == '1':
            server_num = 1
        elif location == '2' or location == '3':
            server_num = 2

        server_address = self.server[server_num-1].ip_address
        self.retrieve_data_from_server(server_address, location)
