# By Rafael Santos
# ID 001034114
# For WGU C950

import csv
from datetime import time
from datetime import datetime
from PackageHashTable import PackageHashTable
from LocationDistanceGraph import LocationDistanceGraph
from Truck import Truck

package_table = PackageHashTable()
location_table = LocationDistanceGraph()


# Resize Table Function takes the old table, and the requested size of the new table, and returns a new table
# Runtime O(n)
def resize_table(old_package_table, package_amount):
    """
    :param package_amount:
    :type old_package_table: PackageHashTable
    """
    # Multiply by 1.3 and convert the float to int
    package_amount_increased_float = package_amount * 1.3
    num = int(round(package_amount_increased_float))

    # Increase the number until it is a prime number
    while True:
        # This checks if the current number is prime. Otherwise, increase the num by 1 and recheck
        if all(temp_int % temp_int for temp_int in range(2, num)):
            print("Prime found: ", num)
            break
        else:
            num += 1

    # Create a new hash table of the larger size
    new_package_table = PackageHashTable(num)

    # Iterate through each index, find every match in the old table, and add to new one
    j = 0
    while j < num:
        j += 1
        if old_package_table.search(i) is not None:
            new_package_table.insert(old_package_table.search(j))

    return new_package_table


# Beginning of main program
# Read CSV file into Hash table
# O(n)
with open('WGUPS Package File (Optimized).csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        package_table.insert(row)

# Initializes the Location graph by loading all locations
# O(n)
address_list = []
with open("WGUPS Addresses Name And Index.csv") as csvfile2:
    readCSV2 = csv.reader(csvfile2, delimiter=',')
    i = 0
    for row in readCSV2:
        address_list.append(row[0])
        location_table.add_location(row[0])
        i += 1

# Loads location distances into the graph
# O(n)
with open("WGUPS Distance Table (Optimized)v7nn.csv") as csvfile3:
    max_column = 0
    temp_location_list = {}
    readCSV3 = csv.reader(csvfile3, delimiter=',')
    loc_1_index = 0
    # Loops 27*27 times, loading  27 distance values for each row and ensuring it is saved correctly
    # Runtime is O(1) since it will always loop 27*27 times (unless the program is modified to add locations)
    for row in readCSV3:
        loc_2_index = 0
        while loc_2_index <= 26:
            location_table.add_edge(address_list[loc_1_index], address_list[loc_2_index], row[loc_2_index])
            loc_2_index += 1
        loc_1_index += 1
# Initialize Truck 1, with default 8am departure time
truck_1 = Truck()
# Initialize truck 2 with 9:05 leaving time
truck_2 = Truck(time(9, 5, 0))

# Temporary list with package to be loaded into each truck (manually presorted)
truck_1_list = [1, 4, 12, 13, 14, 15, 16, 19, 20, 21, 24, 27, 34, 35, 39, 40]
truck_2_list = [3, 5, 6, 7, 8, 10, 18, 25, 26, 29, 30, 31, 32, 36, 37, 38]
truck_3_list = [2, 9, 11, 17, 22, 23, 28, 33]

# Load package into truck 1 and 2
for i in truck_1_list:
    truck_1.load_package(package_table.search(i))
for i in truck_2_list:
    truck_2.load_package(package_table.search(i))

# Create routes for truck 1 and 2
truck_1.create_route(location_table)
truck_2.create_route(location_table)

# Check which of the two trucks arrived back at the hub first. This will become truck 3's leaving time.
truck_1_arrival = truck_1.get_latest_time()
truck_2_arrival = truck_2.get_latest_time()
if truck_1_arrival > truck_2_arrival:
    truck_3 = Truck(truck_2_arrival)
else:
    truck_3 = Truck(truck_1_arrival)
for i in truck_3_list:
    truck_3.load_package(package_table.search(i))
truck_3.create_route(location_table)

# Save total truck mileage
truck_1_mileage = truck_1.get_travel_distance()
truck_2_mileage = truck_2.get_travel_distance()
truck_3_mileage = truck_3.get_travel_distance()

# Start CLI
print("************************************************************")
print("*                C950 WGUPS Routing Software               *")
print("*                     By Rafael Santos                     *")
print("************************************************************")


# UI definitions

# Package Info menu. Allows to see package attributes by ID
def package_info_menu():
    print("\n\n\n")
    print("Package Information")
    while True:
        print("Please enter a package ID (1-40)")
        print("Enter 0 to exit to the main menu.")
        package_user_input = int(input())
        if 1 <= int(package_user_input) <= 40:
            package_info = package_table.search(int(package_user_input))
            print("ID: ", package_info[0])
            print("Address:", package_info[1], ",", package_info[2], ",", package_info[3], package_info[4])
            print("Deadline: ", package_info[5])
            print("Weight (kilos): ", package_info[6])
            print("Special notes: ", package_info[7])
            print("\n")
        elif int(package_user_input) == 0:
            print("Exiting to menu.")
            break
        else:
            print("You have entered an invalid option. Please enter a valid package ID (1-40)\n")


# Truck Info Menu. See packages on each truck, route, and mileage
def truck_info_menu():
    print("\n\n\n")
    print("Truck Information")
    while True:
        print("\n")
        print("Please Select a truck")
        print("(1) Truck 1")
        print("(2) Truck 2")
        print("(3) Truck 3")
        print("(4) Total Truck Mileage")
        print("(0) Exit to Main Menu")
        user_input = int(input())

        # Truck 1
        if int(user_input == 1):
            print("Packages loaded:")
            print(truck_1_list)
            print("Departure Time:", truck_1.get_departure_time())
            print("Route:")
            print("Delivery ID | Address | Timestamp | Package Delivered")
            delivery_log = truck_1.get_delivery_log()
            i = 1
            for item in delivery_log:
                delivery = delivery_log[item]
                timestamp = delivery[1]
                if delivery[2] is None:
                    delivery[2] = "N/A"
                print(str(i), "|", delivery[0], "|", timestamp.strftime("%I:%M%p"), "|", delivery[2])
                i += 1
            print("Deliveries finished at:", truck_1.get_return_time())
            print("Trip Mileage: ", round(truck_1.get_travel_distance(), 1))

        # Truck 2
        elif int(user_input == 2):
            print("Packages loaded:")
            print(truck_2_list)
            print("Departure Time:", truck_2.get_departure_time())
            print("Route:")
            print("Delivery ID | Address | Timestamp | Package Delivered")
            delivery_log = truck_2.get_delivery_log()
            i = 1
            for item in delivery_log:
                delivery = delivery_log[item]
                timestamp = delivery[1]
                if delivery[2] is None:
                    delivery[2] = "N/A"
                print(str(i), "|", delivery[0], "|", timestamp.strftime("%I:%M%p"), "|", delivery[2])
                i += 1
            print("Deliveries finished at:", truck_2.get_return_time())
            print("Trip Mileage: ", round(truck_2.get_travel_distance(), 1))

        # Truck 3
        elif int(user_input == 3):
            print("Packages loaded:")
            print(truck_3_list)
            print("Departure Time:", truck_3.get_departure_time())
            print("Route:")
            print("Delivery ID | Address | Timestamp | Package Delivered")
            delivery_log = truck_3.get_delivery_log()
            i = 1
            for item in delivery_log:
                delivery = delivery_log[item]
                timestamp = delivery[1]
                if delivery[2] is None:
                    delivery[2] = "N/A"
                print(str(i), "|", delivery[0], "|", timestamp.strftime("%I:%M%p"), "|", delivery[2])
                i += 1
            print("Deliveries finished at:", truck_3.get_return_time())
            print("Trip Mileage: ", round(truck_3.get_travel_distance(), 1))

        # Total Mileage
        elif user_input == 4:
            print("Total Trip Mileage")
            print("Truck 1: ", str(round(truck_1_mileage, 1)))
            print("Truck 2: ", str(round(truck_2_mileage, 1)))
            print("Truck 3: ", str(round(truck_3_mileage, 1)))
            print("Total Mileage:", str(round(truck_1_mileage + truck_2_mileage + truck_3_mileage)))

        elif user_input == 0:
            print("Exiting to main menu...")
            break

        else:
            print("Input invalid. Please enter a valid option(1-4,0)")


# Delivery Status menu. See delivery status at a given time
def deliver_status_info():
    print("\n\n\n")
    print("Delivery Status")
    while True:
        print("Enter a time (in the format HH:MM, 24h time) to check package delivery status, or 0 to exit.")
        user_input = input()
        if user_input == str(0):
            print("Exiting to main menu...")
            break
        else:
            print("Package ID | Address | Deadline | Weight| Status")
            try:
                user_time = datetime.strptime(user_input, '%H:%M')
                package_id = 1
                while package_id <= 40:
                    if package_id in truck_1_list:
                        print(truck_1.get_package_info_string(package_id), "|",
                              truck_1.get_truck_package_status(package_id, user_time))
                    elif package_id in truck_2_list:
                        print(truck_2.get_package_info_string(package_id), "|",
                              truck_2.get_truck_package_status(package_id, user_time))
                    elif package_id in truck_3_list:
                        print(truck_3.get_package_info_string(package_id), "|",
                              truck_3.get_truck_package_status(package_id, user_time))
                    package_id += 1
            except ValueError:
                print("The input you entered is invalid. Please enter the time in the format HH:MM (24h time)")


# Main menu
def main_menu():
    while True:
        print("\n\n\n")
        print("Main Menu")
        print("Please enter an option (1-3):")
        print("(1) Package Information: View package attributes by ID.")
        print("(2) Truck Information: See packages on each truck, route info, and total mileage.")
        print("(3) Delivery Status: Check the delivery status of a package with a given time.")
        print("(0) Exit")
        print("")
        user_input = input()
        if user_input == '1':
            package_info_menu()
        elif user_input == '2':
            truck_info_menu()
        elif user_input == '3':
            deliver_status_info()
        elif user_input == '0':
            print("Exiting Application...")
            break
        else:
            print("You have entered an invalid option. Please enter a valid selection (1,2,3)")


# Start Main Menu. This will run indefinitely until program is terminated
main_menu()
