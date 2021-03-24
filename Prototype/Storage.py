import socket
import json

import pymongo
from pymongo import MongoClient


class Storage:
    def __init__(self, server_id, ip_address):
        self.server_id = server_id
        self.weather_stations = []
        self.ip_address = ip_address

    def generate_data_in_weather_stations(self):
        for station in self.weather_stations:
            station.generate_data(10)

    def add_weather_station(self, new_station):
        # Could add weather stations in a dictionary instead, and have name/locaton or id to indicate which to remove
        #  Probably not necesary
        self.weather_stations.append(new_station)
        pass

    def remove_weather_station(self):
        # might not be needed at all
        pass

    def receive_data_from_station_network(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #create UDP socket
        #TODO: not sure if we need sock.bind(('ip', 5555))
        address = ('127.0.0.1', 5555)
        sock.settimeout(1.0) #set timeout value of 1 second

        for station in self.weather_stations:
            sock.sendto(json.dumps({'command':1}), address) #sending request to the weatheer station for command
            #TODO: make a protocol, decide port, commands, json etc.
            #if data is received back from server, then print
            try:
                data = sock.recvfrom(1024)
                j_data = json.loads(data)
                temperature, percipitation = j_data['temperature'], j_data['percipitation'] #get temperature and percipitation values from data
                print("Storage server #" + str(self.server_id) + " weather-station #" + str(
                station.station_id) + " in location: " + station.location_name)
                print(temperature)
                print(percipitation)
            #if data is not received back from server, time out
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
            "Weather station ID": weather_station.station_id,
            "Location": weather_station.location_name,
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
        pass
