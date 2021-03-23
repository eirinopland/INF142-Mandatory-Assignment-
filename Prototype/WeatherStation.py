from time import sleep

from station import StationSimulator

from socket import socket, AF_INET, SOCK_DGRAM


class WeatherStation:
    def __init__(self, station_id, location_name="Bergen"):
        self.bergen_station = StationSimulator(simulation_interval=1)
        # Two lists for temperature and precipitation
        self.temperature = []
        self.precipitation = []
        self.location_name = location_name
        self.station_id = station_id

    def generate_data(self, seconds_to_generate_data):
        # Instantiate a station simulator
        # Turn on the simulator
        self.bergen_station.turn_on()

        # Capture data for 72 hours
        # Note that the simulation interval is 1 second
        for _ in range(seconds_to_generate_data):
            # Sleep for 1 second to wait for new weather data
            # to be simulated
            sleep(1)
            # Read new weather data and append it to the
            # corresponding list
            self.temperature.append(self.bergen_station.temperature)
            self.precipitation.append(self.bergen_station.rain)

        # Shut down the simulation
        self.bergen_station.shut_down()

    def get_data_over_network(self):
        # TODO: Something to send the temperature and precipitation over network
        listOfData = [[self.temperature[i], self.precipitation[i]] for i in range(len(self.temperature))]
        encodedList = []

        for i in listOfData:
            for j in i:
                jByte = str(j).encode()
                encodedList.append(jByte)

        sock = socket(AF_INET, SOCK_DGRAM)

        for i in encodedList:
            # Legg inn addresse/port til riktig storage server, basert på hvilken stasjon data er fra.
            sock.sendto(i, ("Storage Server Address", 5555))
        pass

    def get_data_offline(self):
        # returns the arrays holding temperature and precipitation
        return self.temperature, self.precipitation
