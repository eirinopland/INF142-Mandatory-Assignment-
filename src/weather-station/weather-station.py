import json
from time import sleep
from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM
from station import StationSimulator
from datetime import datetime


class WeatherStation:
    def __init__(self, station_id):
        # Instantiate a weather-station simulator
        self.weather_station = StationSimulator(simulation_interval=1)  # TODO: Sett til 3600 = 1 time
        self.station_id = station_id
        # Turn on the simulator
        self.weather_station.turn_on()


        # sockets:
        self.storage_socket = socket(AF_INET, SOCK_DGRAM)  # UDP socket

        # boolean used to determine if the weather-station is running
        self.running = True

    ################################
    # Main loop and helper methods #
    ################################

    def main(self):
        # Thread(target=self.shutdown).start()

        while self.running:
            self.send_to_storage(self.weather_station.temperature, self.weather_station.rain)
            sleep(1)

        self.weather_station.shut_down()
        exit(0)

    def set_storage_server(self, storage_address):
        self.storage_address = storage_address

    def shutdown(self):
        sleep(3600)
        # shutdown after one hour
        print("received shutdown message - exiting loop")
        self.running = False
        exit(0)

    #########################
    # Communication methods #
    #########################

    def send_to_storage(self, temperature, precipitation):
        data = {"Command": "PUT", "Station ID": self.station_id, "Date": str(datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S")), "Temperature": temperature, "Precipitation": precipitation}

        j_data = json.dumps(data)
        self.storage_socket.sendto(j_data.encode(), self.storage_address)


if __name__ == "__main__":
    station = WeatherStation(1)
    station.set_storage_server(("localhost", 10001))
    station.main()
