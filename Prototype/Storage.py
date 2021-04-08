import json
from datetime import datetime
from socket import socket, AF_INET, SOCK_DGRAM
import threading
from pymongo import MongoClient


class Storage:
    def __init__(self, storage_id):
        self.weather_stations = []
        self.storage_id = storage_id

    def receive_data_from_station_network(self):
        sock = socket(AF_INET, SOCK_DGRAM)  # Create UDP socket
        sock.bind(("localhost", 10000 + self.storage_id))

        station_id, _ = sock.recvfrom(1024)
        station_id = station_id.decode()
        print(station_id)  # This is the ID sent from station at start of each data transfer.
        # TODO: We need to add this to the same doc in database as the data in the following loop.

        while True:
            data, _ = sock.recvfrom(1024)
            j_data = json.loads(data.decode())
            print(station_id, j_data)

            # self.store_data_in_db("SomeStationID", {temperature, precipitation})

    def store_data_in_db(self, weather_station, temperature, precipitation):
        # login details for cluster:
        # TODO Might have separate login or cluster_name details for each server/storage?
        password = "9FcPzJY7ogaHMn8d"
        username = "serverDB"
        cluster_name = "cluster0"
        # Connect to cluster
        client = MongoClient("mongodb+srv://" + username + ":" + password + "@" + cluster_name
                             + ".hjee9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

        new_weather_data = {
            "Weather station ID": weather_station.get_server_id(),
            "Location": weather_station.get_location_name(),
            "Time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "temperature": temperature,
            "precipitation": precipitation
        }

        # Create a new database in your cluster
        database = client.Storage_server_test
        # Create a new collection in you database
        weather_station = database.Weather_station_test
        weather_station.insert_one(new_weather_data)

    def retrieve_data_from_db(self):
        # login details for cluster:
        # TODO Might have separate login or cluster_name details for each server/storage?
        password = "9FcPzJY7ogaHMn8d"
        username = "serverDB"
        cluster_name = "cluster0"
        # Connect to cluster
        client = MongoClient("mongodb+srv://" + username + ":" + password + "@" + cluster_name
                             + ".hjee9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        database = client.Storage_server_test
        # Create a new collection in you database
        weather_station = database.Weather_station_test
        data = weather_station.find({})
        
        for doc in weather_station.find({}):
            print(doc)

        #return data
        
    def handle_FMI_request(self, connection):
        try:
            message = connection.recv(1024)
            j_data = json.loads(message)
            
            if j_data["command"] == 1:
                # data = self.retrieve_data_from_db()
                # message = json.dumps(data)
                message = {"TEST": "TEST"}
                message = json.dumps(message)
                connection.send(message.encode())
            else:
                connection.send(json.dumps({"Error": "Wrong command %d" % j_data['command']}))
        except:
            pass  # TODO: Do something here?
    
    def FMI_thread(self):
        sock = socket()  # Create TCP socket
        server_address = ("localhost", 5000 + self.storage_id)
        sock.bind(server_address)

        # TODO: Set the number of clients waiting for connection that can be queued?
        sock.listen(4)

        while True:
            connection, address = sock.accept()
            try:
                self.handle_FMI_request(connection)
                #print("Connected from", address)
                #self.handle_FMI_request(sock)
                #newSocket.shutdown()
                #newSocket.close()
                #print("Disconnected from", address)
            finally:
                connection.close()


if __name__ == "__main__":
    storage1 = Storage(1)
    # storage1.FMI_thread()
    thread1 = threading.Thread(target=storage1.receive_data_from_station_network)
    thread2 = threading.Thread(target=storage1.FMI_thread)
    thread2.start()
    thread1.start()
