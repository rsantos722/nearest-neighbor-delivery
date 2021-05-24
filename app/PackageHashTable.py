# Chaining Hash Table implementation for WGUPS Packages
class PackageHashTable:

    # Default table size is closest prime to 1.3 times the default amount of packages (53 for the 40 default packages)
    # This ensures no collisions in case of growth
    def __init__(self, table_size=53):
        self.table = []
        for i in range(table_size):
            self.table.append([])

    # Inserts new package into the hash table
    # O(1)
    def insert(self, package):
        # Get first index of the package item list (package ID), mod by table size for bucket, then add it to bucket
        bucket = int(package[0]) % len(self.table)
        bucket_list = self.table[bucket]
        bucket_list.append(package)

    # Searches for package with matching package ID, return it if found, or None if nothing is found. Package id can
    # be entered as either an int or a string of a number. While I could simplify this to accept a certain type,
    # this way there should be less type conversions and it should be easier to pass a value
    # O(1)
    def search(self, package_id):
        # find bucket that has the package based on the ID
        bucket = package_id % len(self.table)
        bucket_list = self.table[bucket]

        # search for the key in bucket list
        for item in bucket_list:
            if str(package_id) in item[0]:
                # If package id matches the first index of package information, its a match
                return item
            else:
                # the package was not found
                return None

    # Removes item with matching key is present
    # O(1)
    def remove(self, package):

        # get bucket where item should be
        bucket = int(package) % len(self.table)
        bucket_list = self.table[bucket]

        # remove item if it exists
        if package in bucket_list:
            bucket_list.remove(package)

    # Returns packages that have the given location as their location
    # O(n)
    def get_package_location_match(self, location):
        matched_packages = []
        for buckets in self.table:
            for item in buckets:
                if item[1] == location:
                    matched_packages.append(item[0])

        return matched_packages

    # Updates a package of given ID with the delivery time
    # O(1)
    def update_package_delivery_status(self, package_id_to_update, package_time):
        # find bucket that has the package based on the ID
        bucket = package_id_to_update % len(self.table)
        bucket_list = self.table[bucket]

        # search for the key in bucket list
        for item in bucket_list:
            if str(package_id_to_update) in item[0]:
                # Update status
                item.append(package_time)

    # Return package status for a given package
    # O(1)
    def get_package_status(self, package_id, timestamp):
        package = None
        # Get package
        bucket = package_id % len(self.table)
        bucket_list = self.table[bucket]

        # search for the key in bucket list
        for item in bucket_list:
            if str(package_id) in item[0]:
                package = item

        # Return package status based on time
        if package[8] > timestamp.time():
            return "AT_HUB"
        elif package[8] <= timestamp.time() < package[9]:
            return "IN_TRANSIT"
        else:
            time_delivered = package[9].strftime("%H:%M")
            return "DELIVERED AT " + time_delivered

    # Returns a formatted string with package info
    # O(1)
    def get_information_string(self, package_id):
        package = []
        # Get package
        bucket = package_id % len(self.table)
        bucket_list = self.table[bucket]

        # search for the key in bucket list
        for item in bucket_list:
            if str(package_id) in item[0]:
                package = item
        # String formatted for console and returned
        return_string = package[0] + " | " + package[1] + ", " + package[2] + ", " + package[3] + " " + package[
            4] + " | " + package[5] + " | " + package[6] + "kg"
        return return_string
