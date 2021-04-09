from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import json

from pymongo import MongoClient


class Storage:
    def __init__(self, storage_id):
        self.stored_time_and_date = []
        self.stored_prec = []
        self.items_in_db = 0
        self.storage_id = storage_id
        self.stored_temp = []

    def main(self):
        # Start one extra thread to handle requests from user-agent
        Thread(target=self.handle_FMI_requests).start()
        self.handle_weather_stations_requests()

    #########################
    # Communication methods #
    #########################

    def handle_weather_stations_requests(self):
        station_socket = socket(AF_INET, SOCK_DGRAM)  # Create UDP socket
        station_socket.bind(("localhost", 10000 + self.storage_id))

        station_id, _ = station_socket.recvfrom(1024)
        # TODO: We need to add this to the same doc in database as the data in the following loop.

        while True:
            message, _ = station_socket.recvfrom(1024)
            self.store_data_in_db(message.decode())

    def handle_FMI_requests(self):
        fmi_socket = socket()  # Create TCP socket
        receive_from_fmi_address = ("localhost", 5000 + self.storage_id)
        fmi_socket.bind(receive_from_fmi_address)

        fmi_socket.listen(1)

        connection, _ = fmi_socket.accept()
        try:
            self.handle_FMI_connections(connection)
        finally:
            connection.close()
            fmi_socket.close()

    def handle_FMI_connections(self, connection):
        while True:
            message = connection.recv(8192)

            if not message:
                break
            elif message.decode() == "GET":
                print("\nReceived request from FMI, transmitting data \n")
                # data_list = []
                # for i in range(self.items_in_db):
                #     data = {}
                #     data["Time and date"] = self.stored_time_and_date[i]
                #     data["Server ID"] = self.storage_id
                #     data["Temperature"] = self.stored_temp[i]
                #     data["Precipitation"] = self.stored_prec[i]
                #     data_list.append(data)

                retrieved_data = self.retrieve_data_from_db()

                print(retrieved_data)

                j_data = json.dumps(retrieved_data)
                connection.sendall(j_data.encode())
            else:
                connection.send(("400\nBad request - un-recognized command: " + message.decode()).encode())
        # connection.close()

    ########################################
    # Storage method (only during runtime) #
    ########################################

    def store_data_in_db_locally(self, data):
        command, station_id, date, time, temperature, precipitation = self.parse_request(data)

        print("Received data, storing locally")
        # TODO: Store in Mongo DB instead
        self.stored_time_and_date.append(date + " - " + time)
        self.stored_temp.append(temperature)
        self.stored_prec.append(precipitation)
        self.items_in_db += 1

    ###################
    # Storage methods #
    ###################

    def store_data_in_db(self, data: str):
        # login details for cluster:
        password = "9FcPzJY7ogaHMn8d"
        username = "serverDB"

        cluster_name = "cluster0"
        # Connect to cluster
        client = MongoClient("mongodb+srv://" + username + ":" + password + "@" + cluster_name
                             + ".hjee9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

        _, station_id, date, time, temperature, precipitation = self.parse_request(data)

        new_weather_data = {
            "Station ID": station_id,
            "Date": date,
            "Time": time,
            "temperature": temperature,
            "precipitation": precipitation
        }

        database_name = "Weather_Station_" + str(station_id)
        database = client[database_name]
        collection_name = "Sensor_Data"
        collection = database[collection_name]

        # Create a new database in your cluster

        # Create a new collection in you database
        # weather-station = database.Weather_station_test
        # weather-station.insert_one(new_weather_data)

        try:
            collection.insert_one(new_weather_data)
        except Exception as e:
            print("Failed to insert ", e)

        print("inserted data into db")

    def retrieve_data_from_db(self, station_id=1):
        # login details for cluster:
        password = "9FcPzJY7ogaHMn8d"
        username = "serverDB"

        cluster_name = "cluster0"
        # Connect to cluster
        client = MongoClient("mongodb+srv://" + username + ":" + password + "@" + cluster_name
                             + ".hjee9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

        database_name = "Weather_Station_" + str(station_id)
        database = client[database_name]
        collection_name = "Sensor_Data"
        collection = database[collection_name]

        data = list(collection.find({}).limit(100))  # .sort("key", DESCENDING)?
        # Should be a list of dicts

        contents = []
        #
        for doc in data:
            contents.append([(doc["Date"] + " " + doc["Time"]), doc["Station ID"], doc["temperature"], doc["precipitation"]])

        # print(data)

        return contents

    ################################
    # Printing and parsing methods #
    ################################

    def parse_request(self, request: str):
        index = request.index("\n")  # the index of the newline
        command = request[:3]  # the command is the first 3 characters of our message i.e. PUT, GET, SET, DEL etc
        station_id = int(request[3 + 1:index])  # ID of the station we're receiving data from
        payload = request[index + 1:]  # payload is the rest of the request list
        date_time = payload[:19]
        date = date_time[:10]
        time = date_time[10 + 1:]
        weather_data = payload[19 + 1:]
        temperature = float(weather_data[:6])
        precipitation = float(weather_data[6 + 1:])

        return command, station_id, date, time, temperature, precipitation

    def pretty_print(self) -> list:
        """
        Method for creating a better formatted output to terminal
        Should be in the format:


        Data from storage server {self.storage_id}:

        dd/mm/yy - 23:59:59 : Temperature = 11.11, Precipitation = 00.00
        dd/mm/yy - 23:59:59 : Temperature = 11.11, Precipitation = 00.00
        etc..

        Returns formatted string
        -------
        TODO:
            - Multiple weather stations
            - Cloud storage / MongoDB
            - Set correct limit in fmi.py for how big this message could be
                - Could check in this method if it reaches near the limit, then return a list of messages
                  that are within that limit which we can send one at a time?
        """
        newline = "\n"
        header = f"Data from storage server {self.storage_id}:"
        message = header + newline
        message_list = []
        for i in range(self.items_in_db):
            message += \
                self.stored_time_and_date[i] + " : " + \
                "Temperature = " + f"{self.stored_temp[i]:06.3F}" + ", " + \
                "Precipitation = " + f"{self.stored_prec[i]:06.3F}" + newline
            message_list.append(message)

        return message_list


if __name__ == "__main__":
    server = Storage(1)
    server.main()
