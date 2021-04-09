from socket import socket


class FMI:
    def __init__(self, storage_info=None):
        if storage_info is None:
            storage_info = {1: ("localhost", 5001), 2: ("localhost", 5002)}
        self._storage_info = ("localhost", 5001)

    def retrieve_data_from_server(self, address):
        sock = socket()
        sock.connect(address)
        # while (text := input("> ").lower()) != "shut down":
        sock.send("GET".encode())  # Command 1 means get all received_message
        received_message = sock.recv(4024) #TODO: Need to determine what this should be, must be enough to transmit all weather-data
        # j_data = json.loads(received_message.decode())
        print(received_message.decode())
        # print(j_data['temperature'], j_data['precipitation'])
        # print(f"From storage-server {server.server_id}:\nTemperature\tPrecipitation\n {received_message}")
        # sock.close()

    def input_from_cli(self, ):
        while True:
            selection = input('(\'ENTER\' to get data)')
            if selection == "":
                self.retrieve_data_from_server(self._storage_info)

            else:
                print('Invalid input, try again!')


            # Trying just to do one of each atm
            # # storage_num = int(selection)
            # if storage_num in self._storage_info:
            #     storage_server_address = self._storage_info.get(storage_num)
            #     self.retrieve_data_from_server(storage_server_address)
            # else:
            #     print('Invalid input, try again!')


if __name__ == "__main__":
    fmi = FMI()
    fmi.input_from_cli()
