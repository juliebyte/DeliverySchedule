# Julie Walin
# Student ID 000951831
# December, 2020

import delivery
import time_utils

package_to_see = 0         # For the selected package_id that user wants to see the status of
user_time_secs = 0         # For the time of the status request
user_choice = 0            # For the selection from the menu

# Displays all packages and their current status.  --->> O(n)
def display_all_packages(time_secs):

    for x in range(1, 41):          # Begins with 1 and ends with 40.
        display_one_package(time_secs, int(x))

# Obtains and prints one package object from the hash table.   --->> O(1)
def display_one_package(time_secs, package_id):

    current_package = delivery.package_hash_table.lookup_value(
        package_id)  # lookup package in the hash table

    if time_utils.hours_HHMMSS_to_seconds(current_package.delivered_time) <= time_secs:
        # This package has been delivered
        current_package.status = "Delivered"
        display_time = current_package.delivered_time   # display the delivered time
    elif time_utils.hours_HHMMSS_to_seconds(current_package.departure_time) <= time_secs:
        # This package is en route
        current_package.status = "En Route"
        display_time = current_package.departure_time    # Display the time loaded onto truck
    elif current_package.status == 'Delayed':
            if time_secs < time_utils.hours_HHMMSS_to_seconds('09:05:00'):
                current_package.status = "Delayed"
                display_time = "        "             # Display a placeholder time as package has not arrived yet
                # This package is delayed
            else:
                current_package.status = "At Hub"
                display_time = "09:05:00"             # Display the time the delayed package arrived at Hub
                # This package is at the Hub
    else:
        current_package.status = "At Hub"
        display_time = "07:00:00"                     # Package assumed to have been at Hub since start of business day
        # This package is at the Hub.

    # Print one line of package data.      --->> O(1)
    formatted_string = "Package ID: {id:02d} |" \
                       " Deadline: {deadline:12s} |" \
                       " {status:18s} |" \
                       "{time:>9s} | " \
                       "{address:23s}" \
                       .format(id=current_package.package_id,
                               deadline=current_package.deadline,
                               status=current_package.status,
                               time=display_time,
                               address=current_package.address)
    print(formatted_string)


print('-----------------------------------------------')
print('                                               ')
print('        WGUPS Delivery Schedule System         ')
print('                                               ')
print('-----------------------------------------------')

# Display the total number of miles needed to deliver all packages.  --->> O(1)
#print("The full route will take ", "{:.2f}".format(delivery.total_distance_traveled), ' miles.')

print('\n', 'Select your choice by typing 1, 2, 3, or quit:')
print('1. Get the status of a specific package at a specific time')
print('2. Get the status of all packages at a specific time')
print('3. Show the mileage')
print('Or type quit to exit the program.\n')

while user_choice != 'quit':

    while True:
        user_choice = input("""Enter your selection here -> """)
        if user_choice in ['quit', '1', '2', '3']:
            break
        else:
            print("Unrecognized entry. Please choose from the menu.")
            continue

    # Display total mileage and miles per each truck.   --->> O(1)
    if user_choice == '3':
        print('Total distance for all trucks = ', "{:.2f}".format( delivery.total_distance_traveled), ' miles.')
        print('Truck 1 total = ', "{:.2f}".format(delivery.truck_1_distance), ' miles.')
        print('Truck 2 total = ', "{:.2f}".format(delivery.truck_2_distance), ' miles.')
        print('Truck 3 total = ', "{:.2f}".format(delivery.truck_3_distance), ' miles.')

    # Obtain a package number from the user.   --->> O(1)
    if user_choice == '1':
        while True:
            try:
                package_to_see = int(input("""Enter the package number you want to see: -> """))
            except ValueError:
                print("Sorry, I didn't understand that package number. Enter an integer.")
                continue
            if package_to_see < 1 or package_to_see > 40:
                print("Package not found. Try another number.")
                continue
            else:
                break

    # Obtain a specific time from the user for the reporting.    --->> O(1)
    if user_choice == '1' or user_choice == '2':
        while True:
            user_time_HHMMSS = input('Please enter a time in HH:MM:SS. (ex: 1:00 PM = 13:00:00): ')
            if time_utils.valid_HHMMSS_input(user_time_HHMMSS):
                # the time entered is valid
                user_time_secs = time_utils.hours_HHMMSS_to_seconds(user_time_HHMMSS)
                break
            else:
                print("Sorry, I didn't understand that time in HH:MM:SS.")
                continue

    # Choose to display either one package or all of the packages and their status.   --->> O(1)
    if user_choice == '1':
        print(' ')               # Print one blank line for formatting
        display_one_package(user_time_secs, package_to_see)
        print(' ')               # Print one blank line for formatting
    else:
        if user_choice == '2':
            print(' ')           # Print one blank line for formatting
            display_all_packages(user_time_secs)
            print(' ')           # Print one blank line for formatting

    # User has chosen to exit.   --->> O(1)
    if user_choice in ['quit', 0, -1]:
        print('Terminating Program')
        exit()
    else:
        continue