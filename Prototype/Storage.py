import socket
import json
from pymongo import MongoClient
from datetime import datetime
#from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM
import threading
import pymongo
from pymongo import MongoClient

class WeatherStation:
    def __init__(self, server_id, ip_address, location_name):
        self.ip_address = (ip_address, 5555)
        self.server_id = server_id
        self.location_name = location_name
    
    def get_server_id(self):
        return self.server_id
    
    def get_ip_address(self):
        return self.ip_address

    def get_location_name(self):
        return self.location_name
    

class Storage:
    def __init__(self):
        self.weather_stations = []
        
        #self.sock.bind(('localhost', 5555))


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
        #address = (weather_stations[0], 5555)
        sock.settimeout(5)
    

        for station in self.weather_stations:
            sock.sendto(json.dumps({'command': 1}).encode(), station.get_ip_address())  # Send request to the weather station for command
            # TODO: make a protocol, decide port, commands, json etc.
            # If data is received back from server, then print
            try:
                data, _ = sock.recvfrom(1024)
                j_data = json.loads(data.decode())
                temperature, precipitation = j_data['temperature'], j_data['precipitation']  # Get temperature and precipitation values from data
                print("Storage server #" + str(station.get_server_id()) + " weather-station #" + str(
                      station.get_server_id()) + " in location: " + station.location_name)
                print("Temperature:\n", temperature)
                print("Precipitation:\n", precipitation)
                self.store_data_in_db(station, temperature, precipitation)
            # If data is not received back from server, time out
            except socket.timeout:
                print('Request timed out')

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
        for doc in weather_station.find({}):
            print(doc)
    
    def handle_FMI_request(self, sock):
        message, address = sock.recv(1024)
        j_data = json.loads(message.decode())
        try:
            if j_data['command'] == 1:
                # Read weather data
                message = json.dumps({"temperature": self.temperature,
                                      "precipitation": self.precipitation})
                self.sock.sendto(message.encode(), address)
                # TODO: Ask TA's if storing data in lists ("temperature", "precipitation") before sending is OK.
                # If not, "handle_request" might need to run "generate_data" for each request, and server must wait.
        except:
            pass
    
    def FMI_thread(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create TCP socket
        sock.bind(('localhost', 5555))

        # Set the number of clients waiting for connection that can be queued
        sock.listen(4)

        # loop waiting for connections (terminate with Ctrl-C)
        try:
            while True:
                newSocket, address = sock.accept()
                print("Connected from", address)
                self.handle_FMI_request(sock)
                # loop serving the new client
                while True:
                    receivedData = newSocket.recv(1024)
                    if not receivedData: break
                    # Echo back the same data you just received
                    newSocket.send(receivedData)
                newSocket.close(  )
                print("Disconnected from", address)
        finally:
            sock.close(  )

if __name__ == "__main__":
    storage = Storage()
    storage.add_weather_station(1, "127.0.0.1", "Bergen")
    thread = threading.Thread(target=storage.FMI_thread(), args=(1,))
    thread.start()
    while True:
        storage.receive_data_from_station_network()


