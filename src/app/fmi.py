from socket import socket
from flask import Flask, render_template
import json

app = Flask(__name__)


class FMI:
    def __init__(self, host, port):
        self._storage_server_address = (host, port)

    def retrieve_data_from_server(self, sock):
        sock.send("GET".encode())
        received_message = sock.recv(8192).decode()
        # Issues might occur if we send too much data ( more than we can receive here )
        return json.loads(received_message)

    def input_from_cli(self):
        sock = socket()
        sock.connect(self._storage_server_address)
        return self.retrieve_data_from_server(sock)


@app.route("/")
def web():
    fmi = FMI("localhost", 5001)
    data = fmi.input_from_cli()
    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(host="localhost")
