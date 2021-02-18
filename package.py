# Created by Julie Walin
# Date December, 2020

# Create a Package object to hold all package information.   --->> O(1)

class Package:
    def __init__(self, package_id, address_id, address, deadline, city, state, zip,
                 weight, truck, status, note, departure_time, delivered_time):
        self.package_id = package_id
        self.address_id = address_id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.state = state
        self.zip = zip
        self.weight = weight
        self.status = status
        self.note = note
        self.departure_time = departure_time
        self.delivered_time = delivered_time
        self.truck = truck


