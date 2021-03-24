# from FMI import *
from Storage import *
from WeatherStation import WeatherStation
import pymongo
from pymongo import MongoClient
# from dotenv import load_dotenv
# load_dotenv()
import os

'''
Setup for the system
- Should create weather stations
- Should create Storage servers
    - and add/assign weather stations to it
'''


if __name__ == "__main__":
    # Creating new weather stations
    server1 = Storage(1)
    station1 = WeatherStation(1)
    server1.add_weather_station(station1)
    station2 = WeatherStation(2)
    server1.add_weather_station(station2)
    station3 = WeatherStation(3)
    server1.add_weather_station(station3)
    station4 = WeatherStation(4)
    server1.add_weather_station(station4)

    # server1.generate_data_in_weather_stations()

    # Create a storage server which should be connected to stations 1-4

    # server1.receive_data_from_station_offline()

    server1.retrieve_data_from_db()

    # print(pymongo.version)

    # client = pymongo.MongoClient(
    #     "mongodb+srv://serverDB:<password>@cluster0.hjee9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    # db = client.test

    # station5 = Weatherstationhub
    # station6 = Weatherstationhub
    # station7 = Weatherstationhub
    # station8 = Weatherstationhub
    #
    # server2 = StorageTest([station1, station2, station3, station4])

    # TODO: Create FMI and pass servers as arguments?


