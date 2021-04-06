from time import sleep

from station import StationSimulator

from socket import socket, AF_INET, SOCK_DGRAM

import json



class WeatherStation:
    def __init__(self, station_id, location_name="Bergen"):
        self.bergen_station = StationSimulator(simulation_interval=1)
        # Two lists for temperature and precipitation
        self.temperature = []
        self.precipitation = []
        self.location_name = location_name
        self.station_id = station_id
        self.generate_data(72)
        # Is this the proper place for running this function? Might need to be run for each request.
        # We might run into problems with requests that takes "seconds_to_generate_data" to finish, might also be OK.

        self.sock = socket(AF_INET, SOCK_DGRAM)  # create UDP socket
        self.sock.bind(('127.0.0.1', 5555))  # assign IP address and port number to socket
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
            # Read new weather data and append it to the corresponding list
            self.temperature.append(self.bergen_station.temperature)
            self.precipitation.append(self.bergen_station.rain)

        # Shut down the simulation
        self.bergen_station.shut_down()

    def handle_request(self):
        message, address = self.sock.recvfrom(1024)
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

    def get_data_over_network(self):
        # The code above replaces the code in this function. Will leave it for now, in case parts of it is needed.
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

station = WeatherStation(1)