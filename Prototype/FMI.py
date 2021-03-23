from socket import socket

class FMI:
    def __init__(self, ):

    def retrieve_data_from_server(self,):
        sock = socket()

        sentence = input("Choose station: ")

        if sentence == '1':
            server_address =  # storage server1
            sock.connect(server_address)
            sock.send(sentence.encode())
            data = sock.recv(1024).decode()
        elif sentence == '2':
            server_address =  # storage server2
            sock.connect(server_address)
            sock.send(sentence.encode())
            data = sock.recv(1024).decode()

        print(f"From Server {sentence}: {data}")

        sock.close()

# if __name__ = "__main__":

