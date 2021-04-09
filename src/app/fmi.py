from socket import socket
from flask import Flask, render_template
import json


class FMI:
    def __init__(self, storage_info=None):
        if storage_info is None:
            storage_info = {1: ("localhost", 5001), 2: ("localhost", 5002)}
        self._storage_info = ("localhost", 5001)

    def retrieve_data_from_server(self, address, sock):
        sock.send("GET".encode())
        received_message = sock.recv(
            8192)  # TODO: Need to determine what this should be, must be enough to transmit all weather-data
        print(received_message.decode())

    def input_from_cli(self, ):
        sock = socket()
        sock.connect(self._storage_info)
        while True:
            selection = input('(\'ENTER\' to get data)')
            if selection == "":
                self.retrieve_data_from_server(self._storage_info, sock)

            else:
                print('Invalid input, try again!')


app = Flask(__name__)

@app.route("/")
def web():
    data = [["dd,mm,yy 23:59:59", "1", "kaldt", "vått"], ["dd,mm,yy 23:59:59", "1", "kaldt", "vått"]]
    return render_template("index.html", data=data)


if __name__ == "__main__":
    fmi = FMI()
    # fmi.input_from_cli()
    app.run(host="localhost")
