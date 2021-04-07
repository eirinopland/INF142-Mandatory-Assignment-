import socket
import json
from pymongo import MongoClient
from datetime import datetime
#from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM
import threading
import pymongo
from pymongo import MongoClient
from time import sleep

class WeatherStation:
    def __init__(self, server_id, ip_address, location_name):
        self.ip_address = (ip_address, 10000+server_id)
        self.server_id = server_id
        self.location_name = location_name
    
    def get_server_id(self):
        return self.server_id
    
    def get_ip_address(self):
        return self.ip_address

    def get_location_name(self):
        return self.location_name


class Storage:
    def __init__(self, storage_id):
        self.weather_stations = []
        self.storage_id = storage_id
        
    def generate_data_in_weather_stations(self):
        for station in self.weather_stations:
            station.generate_data(10)

    def add_weather_station(self, server_id, ip_address, location_name):
        # Could add weather stations in a dictionary instead, and have name/location or id to indicate which to remove
        #  Probably not necessary
        station = WeatherStation(server_id, ip_address, location_name)
        self.weather_stations.append(station)
        #pass

    def remove_weather_station(self):
        # might not be needed at all
        pass

    def receive_data_from_station_network(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create UDP socket
        self.sock.bind(("127.0.0.1", 5555))  # Do we need different sockets/ports for each WS sending data?
        #address = (weather_stations[0], 5555)

        while True:
            # Loop until all data is transferred (72 hours), and then stop? Or run indefinitely?
            data, _ = sock.recvfrom(1024)
            j_data = json.loads(data.decode())
            temperature, precipitation = j_data["temperature"], j_data["precipitation"]
            print("Storage server #" + str(station.get_server_id()) + " weather-station #" + str(
                  station.get_server_id()) + " in location: " + station.location_name)
            print("Temperature:\n", temperature)
            print("Precipitation:\n", precipitation)
            self.store_data_in_db(station, temperature, precipitation)

    def receive_data_from_station_offline(self):
        for station in self.weather_stations:
            temperature, precipitation = station.get_data_offline()
            self.store_data_in_db(station, temperature, precipitation)

    def store_data_in_db(self, weather_station, temperature, precipitation):
        # login details for cluster:
        # TODO Might have separate login or cluster_name details for each server/storage?
        password = "9FcPzJY7ogaHMn8d"
        username = "serverDB"
        cluster_name = "cluster0"
        # Connect to cluster
        client = MongoClient('mongodb+srv://' + username + ':' + password + '@' + cluster_name
                             + '.hjee9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

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
        client = MongoClient('mongodb+srv://' + username + ':' + password + '@' + cluster_name
                             + '.hjee9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
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
           
            # Echo back the same data you just received
            
            if j_data['command'] == 1:
                # Read weather data
                data = self.retrieve_data_from_db()
                print(data)
                message = json.dumps(data)
                connection.send(message)
                # TODO: Ask TA's if storing data in lists ("temperature", "precipitation") before sending is OK.
                # If not, "handle_request" might need to run "generate_data" for each request, and server must wait.
            else:
                connection.send(json.dumps({'Error': 'Wrong command %d' %j_data['command']}))
        except:
            pass #do something here
    
    def FMI_thread(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create TCP socket
        server_address = ('127.0.0.1', 5001)#self.storage_id)
        sock.bind(server_address)

        # Set the number of clients waiting for connection that can be queued
        sock.listen(4)

        # loop waiting for connections (terminate with Ctrl-C)
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
    storage = Storage(1)
    storage.add_weather_station(1, "127.0.0.1", "Bergen")
    thread = threading.Thread(target=storage.FMI_thread)
    thread.start()
    for _ in range(10):
        storage.receive_data_from_station_network()
        sleep(1)
