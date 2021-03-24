
import socket
import json

class Storage:
    def __init__(self, server_id):
        self.server_id = server_id
        self.weather_stations = []

    def generate_data_in_weather_stations(self):
        for station in self.weather_stations:
            station.generate_data(2)

    def add_weather_station(self, new_station):
        # Could add weather stations in a dictionary instead, and have name/locaton or id to indicate which to remove
        #  Probably not necesary
        self.weather_stations.append(new_station)
        pass

    def remove_weather_station(self):
        # might not be needed at all
        pass

    def receive_data_from_station(self):
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
            
            #temperature, percipitation = station.get_data_over_network()
            #print("Storage server #" + str(self.server_id) + " weather-station #" + str(
             #   station.station_id) + " in location: " + station.location_name)
            #print(temperature)
            #print(percipitation)

    def store_data_in_db(self):
        pass

    def retrieve_data_from_db(self):
        pass

    def send_db_data(self):
        pass