from time import sleep

from station import StationSimulator

from socket import socket, AF_INET, SOCK_DGRAM

import json


class WeatherStation:
    def __init__(self, station_id, location_name="Bergen"):
        self.bergen_station = StationSimulator(simulation_interval=1) # sett til 3600 = 1 time
        # Two lists for temperature and precipitation
        self.temperature = []
        self.precipitation = []
        self.location_name = location_name
        self.station_id = station_id
        self.generate_data(72)

        self.sock = socket(AF_INET, SOCK_DGRAM)  # create UDP socket
        self.sock.bind("localhost", 5555)
        while True:
            # continuously handle requests
            self.handle_request()

    def generate_data(self, seconds_to_generate_data):
        # Instantiate a station simulator
        # Turn on the simulator
        self.bergen_station.turn_on()

        # Capture data for "seconds_to_generate_data" hours
        # Note that the simulation interval is 1 second
        for _ in range(seconds_to_generate_data):
            # Sleep for 1 second to wait for new weather data
            # to be simulated
            sleep(1)
            message = json.dumps({"temperature": self.bergen_station.temperature,
                                  "precipitation": self.bergen_station.rain})
            self.sock.sendto(message.encode(), ("localhost", 5555))

        # Shut down the simulation
        self.bergen_station.shut_down()

    def handle_request(self):
        message, address = self.sock.recvfrom(1024)
        j_data = json.loads(message.decode())

    def get_data_offline(self):
        # returns the arrays holding temperature and precipitation
        return self.temperature, self.precipitation


station = WeatherStation(1)