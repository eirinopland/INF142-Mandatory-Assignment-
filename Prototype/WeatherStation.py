import threading
from time import sleep

from station import StationSimulator

from socket import socket, AF_INET, SOCK_DGRAM

import json


class WeatherStation:
    def __init__(self, station_id, location_name="Bergen"):
        self.station1 = StationSimulator(simulation_interval=1)  # TODO: Sett til 3600 = 1 time
        self.location_name = location_name
        self.station_id = station_id
        self.generate_data(72)

    def generate_data(self, seconds_to_generate_data):
        # Turn on the simulator
        self.station1.turn_on()
        sock = socket(AF_INET, SOCK_DGRAM)  # create UDP socket

        id_to_send = str(self.station_id).encode()
        sock.sendto(id_to_send, ("localhost", 10000 + self.station_id))
        # Sends station_id to Storage before transferring data.

        for _ in range(seconds_to_generate_data):
            sleep(1)

            # Package data into json object
            message = json.dumps({"temperature": self.station1.temperature,
                                  "precipitation": self.station1.rain})
            sock.sendto(message.encode(), ("localhost", 10000 + self.station_id))

        # Shut down the simulation
        self.station1.shut_down()


if __name__ == '__main__':
    station1 = WeatherStation(1)
