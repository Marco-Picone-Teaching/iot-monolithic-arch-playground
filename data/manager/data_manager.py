from application.model.device_model import DeviceModel
from application.model.location_model import LocationModel


class DataManager:
    """
    DataManager class is responsible for managing the data of the application.
    Abstracts the data storage and retrieval operations.
    In this implementation everything is stored in memory.
    """

    location_dictionary = {}

    device_timeseries_data = {}

    def init_demo_data(self):
        """Initialize the DataManager with some demo data"""

        # Demo Location
        demo_location = LocationModel("l0001",
                                      "TestBuilding",
                                      48.312321,
                                      10.433423211)

        # Add New Location
        self.add_location(demo_location)

        # Demo Device for the previous location
        demo_device = DeviceModel("d0001",
                                  "demo-device",
                                  demo_location.uuid,
                                  DeviceModel.DEVICE_TYPE_DEFAULT,
                                  "ACME Inc",
                                  "0.0.1beta",
                                  48.312321,
                                  10.433423211)

        # Add New Device
        self.add_device(demo_location.uuid, demo_device)

    # LOCATION MANAGEMENT
    def add_location(self, new_location):

        # Check the correct instance for the variable new_location
        if isinstance(new_location, LocationModel):
            self.location_dictionary[new_location.uuid] = new_location
        else:
            raise TypeError("Error adding new Location ! Only LocationModel are allowed !")

    def update_location(self, updated_location):

        # Check the correct instance for the variable updated_location
        if isinstance(updated_location, LocationModel):
            self.location_dictionary[updated_location.uuid] = updated_location
        else:
            raise TypeError("Error updating the Location ! Only LocationModel are allowed !")

    def remove_location(self, location_uuid):
        if location_uuid in self.location_dictionary.keys():
            del self.location_dictionary[location_uuid]

    def get_location_by_id(self, location_id):
        """Return a location by its id"""
        if location_id in self.location_dictionary:
            return self.location_dictionary[location_id]
        else:
            return None

    def get_all_locations(self):
        """Return a list of all locations"""
        return self.location_dictionary.values()

    # DEVICE MANAGEMENT

    def add_device(self, location_id, new_device):

        # Check the correct instance for the variable new_device
        if isinstance(new_device, DeviceModel):
            # Check if the required Location Id is correct
            if location_id in self.location_dictionary:
                self.location_dictionary[location_id].device_dictionary[new_device.uuid] = new_device
            else:
                raise IndexError("Error Location Id is not correct !")
        else:
            raise TypeError("Error adding new device ! Only DeviceModel are allowed !")

    def update_device(self, location_id, updated_device):
        # Check the correct instance for the variable new_device
        if isinstance(updated_device, DeviceModel):
            # Check if the required Location Id is correct
            if location_id in self.location_dictionary:
                self.location_dictionary[location_id].device_dictionary[updated_device.uuid] = updated_device
            else:
                raise IndexError("Error Location Id is not correct !")
        else:
            raise TypeError("Error adding new device ! Only DeviceModel are allowed !")

    def remove_device(self, location_id, device_uuid):

        # Check if the required Location Id is correct
        if location_id in self.location_dictionary:
            # Retrieve the target location object
            target_location = self.location_dictionary[location_id]

            if device_uuid in target_location.device_dictionary.keys():
                del target_location.device_dictionary[device_uuid]
        else:
            raise IndexError("Error Location Id is not correct !")

    def get_device_by_id(self, device_id):
        """Return a device by its id"""
        for location in self.location_dictionary.values():
            if device_id in location.device_dictionary:
                return location.device_dictionary[device_id]
        return None

    def get_devices_by_location(self, location_id):
        """Return a list of all devices for a given location"""
        if location_id in self.location_dictionary:
            return list(self.location_dictionary[location_id].device_dictionary.values())
        else:
            raise IndexError("Error Location Id is not correct !")

    def add_device_telemetry_data(self, device_id, telemetry_data):
        """Add a new telemetry data for a given device"""
        if device_id not in self.device_timeseries_data:
            self.device_timeseries_data[device_id] = []
        self.device_timeseries_data[device_id].append(telemetry_data)

    def get_telemetry_data_by_device_id(self, device_id):
        """Return the telemetry data for a given device"""
        if device_id in self.device_timeseries_data:
            return self.device_timeseries_data[device_id]
        else:
            return None

    def is_location_registered(self, location_id):
        """Check if a location is registered"""
        return location_id in self.location_dictionary