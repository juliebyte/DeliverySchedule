# Julie Walin
# December, 2020

# This module processes the deliveries of the packages.
import csv
from hash_table import HashTable
from package import Package
import time_utils

package_hash_table = HashTable()
TRUCK_SPEED_MPH = 18      # Trucks travel at an average speed of 18 mph
addresses_all = []        # an array to hold all of the addresses and their address_id.
distances_all = []        # an array to hold all of the rows of distance data - each row is also an array
total_distance_traveled = 0.0     # to store the total distance traveled by all of the trucks


# Starting distances file.   --->> O(n)
with open('./data_files/distances_file.csv', encoding="utf-8-sig", mode='r') as csvfile:
    read_csv = csv.reader(csvfile, delimiter=',')

    distances_count = 0
    for row in read_csv:
        distance_row = []                      # Define a new, empty array
        for column in row:
            distance_row.append(float(column))    # The whole row array is ready and is added to the distances_all array
        distances_all.append(distance_row)
        distances_count += 1

# Starting delivery addresses file.      --->> O(n)
with open('./data_files/addresses_file.csv', encoding="utf-8-sig", mode='r') as csvfile:
    read_csv = csv.reader(csvfile, delimiter=',')

    addresses_count = 0
    for row in read_csv:
        address_row = []  # Define a new, empty array
        for column in row:
            address_row.append(column)  # The whole row array is ready and is added to the addresses_all array

        addresses_all.append(address_row)
        addresses_count += 1

package_hash_table = HashTable()    # instantiate an instance of Hash_Table for storing packages
first_truck = []          # packages to be loaded on first truck, random order
second_truck = []         # packages to be loaded on second truck, random order
third_truck = []          # packages to be loaded of third truck, random order
working_truck = []        # packages to be delivered from current truck

# Match the address on the package to an address in the addresses list
# to get the index number of the address for delivery  --->> O(n)
def get_address_id(address):
    for x in addresses_all:
        if address == x[1]:    # If the delivery address is found
            return int(x[0])   # Return the corresponding address_id which will be used as an index

# Read CSV file of package data      --->> O(n)
with open('./data_files/package_file.csv', encoding="utf-8-sig", mode='r') as csvfile:
    read_csv_package = csv.reader(csvfile, delimiter=',')

    for row in read_csv_package:
        package_id = int(row[0])
        address = row[1]
        city = row[2]
        state = row[3]
        zip = row[4]
        deadline = row[5]
        package_weight = row[6]
        note = row[7]
        truck = 0
        package_status = 'At Hub'
        departure_time = "99:99:99"             # Placeholder time
        delivered_time = "99:99:99"             # Placeholder time
        address_id = get_address_id(address)    # Look up address in addresses_all list

        if note[0:7] == 'Delayed':              # If the package is delayed
            package_status = 'Delayed'          # Save "Delayed" in the status

        # Create a package object
        currentPackage = Package(package_id, address_id, address, deadline, city, state, zip,
                             package_weight, truck, package_status, note, departure_time, delivered_time)


        # Add the package object to the hash table
        package_hash_table.insert(package_id, currentPackage)

        if package_id in {1, 13, 14, 15, 16, 19, 20, 21, 29, 30, 39, 40, 27, 33, 35, 37}:
            first_truck.append(package_id)
        elif package_id in {3, 6, 10, 11, 18, 22, 23, 24, 25, 26, 28, 31, 32, 34, 36, 38}:
            second_truck.append(package_id)
        else:
            third_truck.append(package_id)  # 2, 4, 5, 7, 8, 9, 10, 12, 17

first_truck_start_secs = 28800   # 8:00 AM in seconds
second_truck_start_secs = 33000  # 9:10 AM in seconds
third_truck_start_secs = 39600   # 11:00 AM in seconds
truck_1_distance = 0.0    # total distance for truck 1
truck_2_distance = 0.0    # total distance for truck 2
truck_3_distance = 0.0    # total distance for truck 3


# This module is used to deliver the packages that are loaded on one truck.
# It is re-used for all trucks.
# This module uses a greedy algorithm to choose which package to deliver next.

# In every case, the truck starts at the hub.
# All packages are searched to find the one closest to the hub.
# That closest package is delivered and removed from the list of packages on the truck.
# The current location of the truck is now the location where that package was delivered.
# Packages are again searched for the nearest delivery location, continuing
# until all packages have been delivered.
# Time Complexity for the section is --->> O(n^2) due to the nested loop.

def deliver_one_truck(working_truck, working_time, working_truck_number):

    loading_time = working_time      # Get the time the truck started being loaded
    shortest_package_id = -1         # Just to initialize
    current_location_index = 0       # Starting the location at index 0 for the Hub
    pkg_delivered_count = 0          # For counting successful deliveries
    destination_address_index = -1   # Where this package is to be delivered
    truck_distance = 0.0             # For accumulating the distance a truck traveled in miles

    # Greedy Algorithm.  --->> O(n^2)
    while len(working_truck) > 0:
        shortest = 900000.0
        for pkg in working_truck:  # go through all of the packages that are on the truck
            # lookup the package in the hash table and create an instance
            current_package = package_hash_table.lookup_value(pkg)
            destination_address_index = current_package.address_id
            # distance is the distance from the current location of the truck to the current package
            distance = (distances_all[current_location_index][destination_address_index])
            if distance < shortest:
                shortest = distance
                shortest_package_id = current_package.package_id

        # Remove the package to be delivered from the truck list
        # Add a timestamp to the package object for delivery time
        # Change the package status to delivered
        if len(working_truck) > 0:
            working_truck.remove(shortest_package_id)  # Remove this package from truck is being delivered now
            current_package = package_hash_table.lookup_value(
                shortest_package_id)  # lookup package in the hash table
            destination_address_index = current_package.address_id
            package_time_hrs = shortest / TRUCK_SPEED_MPH  # how much time this delivery took
            package_time_secs = time_utils.hours_decimal_to_seconds(package_time_hrs)
            working_time += package_time_secs
            current_package.departure_time = time_utils.seconds_to_HHMMSS(loading_time)  # Time the package was put on truck
            current_package.delivered_time = time_utils.seconds_to_HHMMSS(working_time)  # Time of delivery
            current_package.truck = working_truck_number      # Record which truck delivered the package

            truck_distance += shortest     # Accumulate total distance for a truck in miles
            # Display the time each package was delivered
            #print('Package ', shortest_package_id, ' delivered at ', current_package.delivered_time)

            package_hash_table.update_value(shortest_package_id,
                                        current_package)  # Update the package that was just delivered
            pkg_delivered_count += 1

            current_location_index = destination_address_index  # Now the truck has moved to the new address
            # that was just delivered so it needs a new current_location_index

    # Truck 1 must return to the hub, so add the mileage from the last delivery to hub. --->> O(1)
    if working_truck_number == 1:
        if len(working_truck) == 0:
            distance_to_hub = float((distances_all[current_location_index][0]))
            truck_distance += distance_to_hub
            package_time_hrs = distance_to_hub / TRUCK_SPEED_MPH  # how much time this delivery took
            package_time_secs = time_utils.hours_decimal_to_seconds(package_time_hrs)
            working_time += package_time_secs
            print('*****First truck returned to hub at ', time_utils.seconds_to_HHMMSS(working_time))
    if working_truck_number != 1:
        if len(working_truck) == 0:
            print('*****Truck ', working_truck_number, ' finished at ', time_utils.seconds_to_HHMMSS(working_time))

    print(pkg_delivered_count, 'packages delivered by this truck')
    return truck_distance

# Deliver the first truck's packages.
# --->> O(1)
truck_1_distance = deliver_one_truck(first_truck, first_truck_start_secs, 1)

# --->> O(1)
# Second truck can't leave until packages 6, 25, 28, and 32 arrive at the Hub at 9:05.
if second_truck_start_secs >= 32700:       # If current time is > or = 9:05 AM
    truck_2_distance = deliver_one_truck(second_truck, second_truck_start_secs, 2)

# Driver 1 has returned and will deliver the contents of truck #3.
# On or after 10:20, the address of Package 9 will be corrected to 410 S State St.
# --->> O(1)
if third_truck_start_secs >= 37200:                        # If current time is > or = 10:20 AM
    package_to_change = package_hash_table.lookup_value(9)  # Lookup package in the hash table
    package_to_change.address = '410 S State St'           # Update to the new delivery address
    package_to_change.address_id = get_address_id(package_to_change.address)   # Look up the new address_id
    package_hash_table.update_value(9, package_to_change)   # Update the delivery address in the hash table

truck_3_distance = deliver_one_truck(third_truck, third_truck_start_secs, 3)   # --->> O(1)

total_distance_traveled = truck_1_distance + truck_2_distance + truck_3_distance
# Display the total number of miles needed to deliver all packages.
print("The full route took ", "{:.2f}".format(total_distance_traveled), ' miles. \n')
