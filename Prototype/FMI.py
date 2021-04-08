from socket import socket
import json

class FMI:
    def __init__(self, storage_info: dict = {1: ("localhost", 5001), 2: ("localhost", 5002)}):
        self._storage_info = storage_info

    def retrieve_data_from_server(self, address):
        sock = socket()
        sock.connect(address)
        #while (text := input("> ").lower()) != "shut down":
        sock.send(json.dumps({'command': 1}).encode())  # Command 1 means get all data
        data = sock.recv(1024)
        j_data = json.loads(data.decode())
        print(j_data)
        #print(j_data['temperature'], j_data['precipitation'])
        #print(f"From storage {server.server_id}:\nTemperature\tPrecipitation\n {data}") 
        sock.close()

    def input_from_cli(self,):
        while True:
            storage_str = input('Choose storage 1 or 2 (\'ENTER\' to exit): ')
            if storage_str == "":
                break
            storage_num = int(storage_str)
            if storage_num in self._storage_info:
                server = self._storage_info.get(storage_num)
                self.retrieve_data_from_server(server)
            else:
                print('Invalid input, try again!')


if __name__ == "__main__":
    fmi = FMI()
    fmi.input_from_cli()
