import datetime
from collections import OrderedDict
from LocationDistanceGraph import LocationDistanceGraph
from PackageHashTable import PackageHashTable
from datetime import time


class Truck:

    def __init__(self, leaving_time=time(8, 0, 0)):
        self.loading_time = leaving_time
        self.package_list = PackageHashTable()
        # Location List: Key is location, bool for delivery status
        self.location_list = {"HUB": True}
        self.location_graph = LocationDistanceGraph()
        self.delivery_log = OrderedDict()
        # Key is delivery ID, then location, time of the delivery, and the package ID
        self.delivery_log = {0: ["HUB", leaving_time, None]}
        self.return_time = None
        self.amount_of_packages = 0
        self.total_travel_distance: float = 0

    # Loads a package with a given ID. Searches for the package from PackageHashTable
    # O(1)
    def load_package(self, package):
        package.append(self.loading_time)
        self.package_list.insert(package)
        self.location_list[package[1]] = False
        self.amount_of_packages += 1

    # Creates a Nearest Neighbor delivery route using the loaded packages.
    # Runtime: O(n^2)
    def create_route(self, location_graph_initialized):

        # Initializing
        self.location_graph = location_graph_initialized
        current_location = "HUB"
        temp = self.delivery_log[0]
        current_time = temp[1]
        i = 0
        min_distance = []
        delivery_id = 1

        # Start of the actual calculations
        while i < self.amount_of_packages:

            # Find nearest next stop
            # Get the list of location distances from the current location
            next_stop_distance_list = self.location_graph.get_edge_length(current_location)

            # Holds the location and distance of the trip. Set to arbitrary 100 which will always be overwritten
            min_distance = ["Temp", 100]

            # Iterate through the list. Check if the location is somewhere we need to go
            for distance_list_item in next_stop_distance_list:
                # if we need to go to that location, check if the distance is smaller than the current min_distance
                if (distance_list_item[0], False) in self.location_list.items() and float(distance_list_item[1]) < \
                        float(min_distance[1]):
                    # Save this location as the next stop
                    min_distance = distance_list_item

            # Calculate the time to the next stop (18mph) in minutes
            self.total_travel_distance += float(min_distance[1])
            time_spent_value = (float(min_distance[1]) / 18) * 60
            time_spent_object = datetime.timedelta(minutes=time_spent_value)
            date_time_object = datetime.datetime.combine(datetime.date(1, 1, 1), current_time)
            current_time = (time_spent_object + date_time_object).time()

            # Check which packages will be delivered. This only returns a list of package ID.
            packages_to_deliver = self.package_list.get_package_location_match(min_distance[0])

            # Log the trip, with current distance, time, and the delivered package
            for package in packages_to_deliver:
                self.package_list.update_package_delivery_status(int(package), current_time)
                self.delivery_log[delivery_id] = [min_distance[0], current_time, package]
                delivery_id += 1
                i += 1

            # Mark the location as visited
            self.location_list[min_distance[0]] = True

            # Update the current package
            current_location = min_distance[0]

        # Loop over, last trip is back to HUB
        next_stop_distance_list = self.location_graph.get_edge_length(current_location)
        for location in next_stop_distance_list:
            if location[0] == "HUB":
                min_distance = location
        time_spent_value = (float(min_distance[1]) / 18) * 60
        time_spent_object = datetime.timedelta(minutes=time_spent_value)
        date_time_object = datetime.datetime.combine(datetime.date(1, 1, 1), current_time)
        current_time = (time_spent_object + date_time_object).time()

        self.delivery_log[delivery_id] = [min_distance[0], current_time, None]
        self.return_time = current_time

    # Getters for certain attributes

    def get_latest_time(self):
        return self.return_time

    def get_travel_distance(self):
        return self.total_travel_distance

    def get_departure_time(self):
        return self.loading_time.strftime("%I:%M%p")

    def get_return_time(self):
        return self.return_time.strftime("%I:%M%p")

    def get_delivery_log(self):
        return self.delivery_log

    def get_truck_package_status(self, package_id, timestamp):
        return self.package_list.get_package_status(package_id, timestamp)

    def get_package_info_string(self, package_id):
        return self.package_list.get_information_string(package_id)
