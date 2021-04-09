from socket import socket

from bson import json_util
from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

class FMI:
    def __init__(self, storage_info=None):
        if storage_info is None:
            storage_info = {1: ("localhost", 5001), 2: ("localhost", 5002)}
        self._storage_info = ("localhost", 5001)

    def retrieve_data_from_server(self, address, sock):
        sock.send("GET".encode())
        received_message = sock.recv(
            8192).decode()  # TODO: Need to determine what this should be, must be enough to transmit all weather-data

        # received_message = json.loads(json_util.dumps(received_message))
        # print(received_message)

        return json.loads(received_message)

    def input_from_cli(self):
        sock = socket()
        sock.connect(self._storage_info)
        return self.retrieve_data_from_server(self._storage_info, sock)

@app.route("/")
def web():
    fmi = FMI()
    data = fmi.input_from_cli()
    data1 = [["dd,mm,yy 23:59:59","1", "kaldt", "vått"],["dd,mm,yy 23:59:59","1", "kaldt", "vått"]]
    print(data)

    return render_template("index.html", data=data)


if __name__ == "__main__":

    app.run(host="localhost")

