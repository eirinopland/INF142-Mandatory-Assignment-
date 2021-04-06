from socket import socket


class FMI:
    def __init__(self, server):
        self.server = server

    def retrieve_data_from_server(self, server, location):
        #sock = socket()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server)
        while (text := input("> ").lower()) != "shut down":
        sock.send(json.dumps({'command': location}).encode())
        #sock.send(location.encode())
        data = sock.recv(1024)
        j_data = json.loads(data.decode())
        print(j_data['temperature'], j_data['precipitation'])
        #print(f"From storage {server.server_id}:\nTemperature\tPrecipitation\n {data}") 
        sock.close()


    def input_from_cli(self,):

        servers_dict = {1: '127.0.0.1', 2: '127.0.0.1'}

        while True:
            storage_num = int(input('Choose storage (1 or 2): '))

            if storage_num in servers_dict:
                server = servers_dict.get(storage_num)
                print(server)

            else:
                print('Invalid input, try again!')

            if not storage_num:
                break
            else:
                continue
        
        server = ("localhost", 10000)
        self.retrieve_data_from_server(server, location)

        #server_address = self.server[server_num-1].ip_address
        #self.retrieve_data_from_server(server_address, location)
