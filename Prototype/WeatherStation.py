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

    def generate_data(self, seconds_to_generate_data):
        # Instantiate a station simulator
        # Turn on the simulator
        self.bergen_station.turn_on()
        sock = socket(AF_INET, SOCK_DGRAM)  # create UDP socket

        id_to_send = str(self.station_id).encode()
        sock.sendto(id_to_send, ("localhost", 5555))  # Sends station_id to Storage before transferring data.

        # Capture data for "seconds_to_generate_data" hours
        # Note that the simulation interval is 1 second
        for _ in range(seconds_to_generate_data):
            # Sleep for 1 second to wait for new weather data
            # to be simulated
            sleep(1)
            message = json.dumps({"temperature": self.bergen_station.temperature,
                                  "precipitation": self.bergen_station.rain})
            sock.sendto(message.encode(), ("localhost", 5555))

        # Shut down the simulation
        self.bergen_station.shut_down()

    def get_data_offline(self):
        # returns the arrays holding temperature and precipitation
        return self.temperature, self.precipitation


station = WeatherStation(1)
