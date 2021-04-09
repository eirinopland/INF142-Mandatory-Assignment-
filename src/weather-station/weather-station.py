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
        Thread(target=self.shutdown).start()

        while self.running:
            self.send_to_storage(self.weather_station.temperature, self.weather_station.rain)
            sleep(10)

        self.weather_station.shut_down()
        exit(0)

    def set_storage_server(self, storage_address):
        self.storage_address = storage_address

    def shutdown(self):
        # TODO: Wait for shutdown request from server instead of a set timer?
        sleep(3600)
        # shutdown after one hour
        print("received shutdown message - exiting loop")
        self.running = False
        exit(0)

    #########################
    # Communication methods #
    #########################

    def send_to_storage(self, temperature, precipitation):
        # TODO: Use json instead
        #             # Package data into json object
        #             message = json.dumps({"temperature": self.station1.temperature,
        #                                   "precipitation": self.station1.rain})
        #             sock.sendto(message.encode(), ("localhost", 10000 + self.station_id))

        data = \
            ("PUT" + " " + f"{self.station_id:02d}" + "\n" + str(datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S")) + " " + f"{temperature:06.3F}" + " " + f"{precipitation:06.3F}")

        bytes = data.encode()

        self.storage_socket.sendto(bytes, self.storage_address)
        # response, _  = self._sock.recvfrom(1024)
        # print(response.decode())


if __name__ == "__main__":
    station = WeatherStation(1)
    station.set_storage_server(("localhost", 10001))
    station.main()
