from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import json

from pymongo import MongoClient


class Storage:
    def __init__(self, storage_id):
        self.storage_id = storage_id

    def main(self):
        # Start one extra thread to handle requests from user-agent
        Thread(target=self.handle_FMI_requests).start()
        self.handle_weather_stations_requests()

    #########################
    # Communication methods #
    #########################

    def handle_weather_stations_requests(self):
        station_socket = socket(AF_INET, SOCK_DGRAM)  # Create UDP socket
        station_socket.bind(("localhost", 10000 + self.storage_id))
        data_list = []

        while True:
            message, _ = station_socket.recvfrom(1024)
            message = json.loads(message.decode())
            if message["Command"] == "PUT":
                message.pop("Command", None)
                data_list.append(message)  # Stores data on server
                print("Received data, storing locally")

            self.store_data_in_db(message)

    def handle_FMI_requests(self):
        fmi_socket = socket()  # Create TCP socket
        receive_from_fmi_address = ("localhost", 5000 + self.storage_id)
        fmi_socket.bind(receive_from_fmi_address)

        fmi_socket.listen(1)

        connection, _ = fmi_socket.accept()
        try:
            self.handle_FMI_connections(connection)
        finally:
            connection.close()
            fmi_socket.close()

    def handle_FMI_connections(self, connection):
        while True:
            message = connection.recv(8192)

            if not message:
                break
            elif message.decode() == "GET":
                print("\nReceived request from FMI, transmitting data \n")

                retrieved_data = self.retrieve_data_from_db()

                j_data = json.dumps(retrieved_data)
                connection.sendall(j_data.encode())
            else:
                connection.send(("400\nBad request - un-recognized command: " + message.decode()).encode())
        connection.close()

    ###################
    # Storage methods #
    ###################

    def store_data_in_db(self, data):
        # login details for cluster:
        password = "9FcPzJY7ogaHMn8d"
        username = "serverDB"

        cluster_name = "cluster0"
        # Connect to cluster
        client = MongoClient("mongodb+srv://" + username + ":" + password + "@" + cluster_name
                             + ".hjee9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

        database_name = "Weather_Station_" + str(data["Station ID"])
        database = client[database_name]
        collection_name = "Sensor_Data"
        collection = database[collection_name]

        try:
            collection.insert_one(data)
        except Exception as e:
            print("Failed to insert ", e)

        print("inserted data into db")

    def retrieve_data_from_db(self, station_id=1):
        # login details for cluster:
        password = "9FcPzJY7ogaHMn8d"
        username = "serverDB"

        cluster_name = "cluster0"
        # Connect to cluster
        client = MongoClient("mongodb+srv://" + username + ":" + password + "@" + cluster_name
                             + ".hjee9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

        database_name = "Weather_Station_" + str(station_id)
        database = client[database_name]
        collection_name = "Sensor_Data"
        collection = database[collection_name]

        data = list(collection.find({}).limit(50)) #.sort("Date", DESCENDING) #( appears to do this already)

        contents = []

        for doc in data:
            contents.append([doc["Date"], doc["Station ID"], doc["Temperature"], doc["Precipitation"]])

        return contents


if __name__ == "__main__":
    server = Storage(1)
    server.main()
