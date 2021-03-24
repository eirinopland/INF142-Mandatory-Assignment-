from socket import socket

class FMI:          #trenger man class hvis det bare skal være 1 FMI som kjører fra CLI?
    def __init__(self, ):
        pass

    sock = socket()
    def retrieve_data_from_server(self, server,location, month): #

        address = server.address #?? kalle på server klassen for å finne addressen ? Ha en input først eventuelt som sender til denne funk
        sock.connect(address)
        sock.send(sentence.encode())
        data = sock.recv(1024).decode()

        print(f"From storage {server.id}:\nTemperature\tPrecipitation\n {data}") #hvordan kommer data inn? Printe så det blir pent

        sock.close()


    def input_from_cli(self,): #passe på at det er gyldig input
        server = int(input("Choose storage server: "))  #skal vi spørre om storage eller location?
        location = input("Location: ")
        month = input("Month: ")
        return server, location, month

if __name__ = "__main__":
    server, location, month = input_from_cli()
    retrieve_data_from_server(server,location,month)

