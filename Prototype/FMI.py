import socket
import json

class FMI:
    def __init__(self, server):
        self.server = server

    def retrieve_data_from_server(self, server):
        #sock = socket()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (server['ip'], server['port'])
        sock.connect(address)
        #while (text := input("> ").lower()) != "shut down":
        sock.send(json.dumps({'command': 1}).encode()) #command 1 means get all data
        data = sock.recv(5120)
        j_data = json.loads(data.decode())
        print(j_data['temperature'], j_data['precipitation'])
        #print(f"From storage {server.server_id}:\nTemperature\tPrecipitation\n {data}") 
        sock.close()

    def input_from_cli(self,):

        servers_dict = {1: {'ip': '127.0.0.1', 'port': 5001}, 2: {'ip': '127.0.0.1', 'port': 5002}}

        while True:
            storage_num = int(input('Choose storage (1 or 2): '))
            if storage_num in servers_dict:
                server = servers_dict.get(storage_num)
                print(server)
                self.retrieve_data_from_server(server)
            else:
                print('Invalid input, try again!')
            if not storage_num:
                break
            else:
                continue
        
        self.retrieve_data_from_server(server)

fmi = FMI(1)
fmi.input_from_cli()