from application.model.device_model import DeviceModel
from application.model.location_model import LocationModel
from communication.mqtt.dto.telemetry_message import TelemetryMessage
from data.manager.data_manager import DataManager


class CoreManager:
    """
    Core Manager class that handles the core functionality of the application
    Main methods re-call the data manager methods to decouple the core functionality from the data management
    Additional dedicated methods are used to handle telemetry data from devices with a specific application logic
    """

    def __init__(self, data_manager: DataManager):
        """Initialize the CoreManager with a Data Manager"""
        self.data_manager = data_manager

    def add_location(self, new_location: LocationModel):
        """Add a new location using the data manager"""
        self.data_manager.add_location(new_location)

    def update_location(self, updated_location: LocationModel):
        """Update a location using the data manager"""
        self.data_manager.update_location(updated_location)

    def remove_location(self, location_uuid: str):
        """Remove a location using the data manager"""
        self.data_manager.remove_location(location_uuid)

    def get_location_by_id(self, location_id):
        """Return a location by its id"""
        return self.data_manager.get_location_by_id(location_id)

    def get_all_locations(self):
        """Return a list of all locations"""
        return self.data_manager.get_all_locations()

    def add_device(self, location_id: str, new_device: DeviceModel):
        """Add a new device using the data manager"""
        self.data_manager.add_device(location_id, new_device)

    def update_device(self, location_id: str, updated_device: DeviceModel):
        """Update a device using the data manager"""
        self.data_manager.update_device(location_id, updated_device)

    def remove_device(self, location_id: str, device_uuid: str):
        """Remove a device using the data manager"""
        self.data_manager.remove_device(location_id, device_uuid)

    def get_device_by_id(self, device_id: str):
        """Return a device by its id"""
        return self.data_manager.get_device_by_id(device_id)

    def get_devices_by_location(self, location_id: str):
        """Return a list of devices by location"""
        return self.data_manager.get_devices_by_location(location_id)

    def add_device_telemetry_data(self, device_id: str, telemetry_data: TelemetryMessage):
        """Add telemetry data for a device using the data manager"""
        self.data_manager.add_device_telemetry_data(device_id, telemetry_data)

    def handle_mqtt_device_telemetry_data(self, device_id: str, device_telemetry_data: TelemetryMessage):
        """ Handle telemetry data from device """

        # Check request not None and instance of TelemetryMessage
        if device_telemetry_data is None or not isinstance(device_telemetry_data, TelemetryMessage):
            raise ValueError("Invalid TelemetryMessage")
        else:

            # If the device is registered, update the telemetry data
            if self.data_manager.get_device_by_id(device_id) is not None:
                self.data_manager.add_device_telemetry_data(device_id, device_telemetry_data)
                print(f'Telemetry data received from device {device_id}')
            else:
                raise ValueError("Device not registered")

    def get_telemetry_data_by_device_id(self, device_id: str):
        """
        Get telemetry data by device id from data manager
        :param device_id: Device id associated with telemetry data
        :return: List of telemetry data
        """
        return self.data_manager.get_telemetry_data_by_device_id(device_id)

    def is_location_registered(self, location_id: str):
        """Check if a location is registered"""
        return self.data_manager.is_location_registered(location_id)