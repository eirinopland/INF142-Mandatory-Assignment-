from time import sleep

from station import StationSimulator

from socket import socket, AF_INET, SOCK_DGRAM

if __name__ == "__main__":

    # Instantiate a station simulator
    bergen_station = StationSimulator(simulation_interval=1)
    # Turn on the simulator
    bergen_station.turn_on()

    # Two lists for temperature and precipitation
    temperature = []
    precipitation = []

    # Capture data for 72 hours
    # Note that the simulation interval is 1 second
    for _ in range(4):
        # Sleep for 1 second to wait for new weather data
        # to be simulated
        sleep(1)
        # Read new weather data and append it to the
        # corresponding list
        temperature.append(bergen_station.temperature)
        precipitation.append(bergen_station.rain)

    # Shut down the simulation
    bergen_station.shut_down()

    # Print the collected data
    print("Temperature\tPrecipitation")
    for t, p in zip(temperature, precipitation):
        print(t, "\t\t", p)

    listOfData = tuple(zip(temperature, precipitation))
    encodedList = []

    print(listOfData)

    sock = socket(AF_INET, SOCK_DGRAM)

    # Legg inn addresse til riktig storage server, basert på hvilken stasjon data er fra.
    sock.sendto(encodedList, ("Storage Server Address", 5555))


