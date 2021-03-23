
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
        # TODO: call get_data_over_network instead of offline temporary version
        for station in self.weather_stations:
            temperature, percipitation = station.get_data_offline()
            print("Storage server #" + str(self.server_id) + " weather-station #" + str(
                station.station_id) + " in location: " + station.location_name)
            print(temperature)
            print(percipitation)

    def store_data_in_db(self):
        pass

    def retrieve_data_from_db(self):
        pass

    def send_db_data(self):
        pass
