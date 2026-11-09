from iot_monolithic_playground.application.model.device_model import DeviceModel
from iot_monolithic_playground.application.model.location_model import LocationModel
from iot_monolithic_playground.application.model.telemetry_model import TelemetryModel
from iot_monolithic_playground.data.data_manager import DataManager


class CoreManager:
    """
    Core Manager class that handles the core functionality of the application
    Main methods re-call the data manager methods to decouple the core functionality from the data management
    Additional dedicated methods are used to handle telemetry data from devices with a specific application logic
    """

    def __init__(self, data_manager: DataManager) -> None:
        """Initialize the CoreManager with a Data Manager"""
        self.data_manager = data_manager

    def add_location(self, new_location: LocationModel) -> None:
        """Add a new location using the data manager"""
        self.data_manager.add_location(new_location)

    def update_location(self, updated_location: LocationModel) -> None:
        """Update a location using the data manager"""
        self.data_manager.update_location(updated_location)

    def remove_location(self, location_uuid: str) -> None:
        """Remove a location using the data manager"""
        self.data_manager.remove_location(location_uuid)

    def get_location_by_id(self, location_id: str) -> LocationModel | None:
        """Return a location by its id"""
        return self.data_manager.get_location_by_id(location_id)

    def get_all_locations(self) -> list[LocationModel]:
        """Return a list of all locations"""
        return self.data_manager.get_all_locations()

    def add_device(self, location_id: str, new_device: DeviceModel) -> None:
        """Add a new device using the data manager"""
        self.data_manager.add_device(location_id, new_device)

    def update_device(self, location_id: str, updated_device: DeviceModel) -> None:
        """Update a device using the data manager"""
        self.data_manager.update_device(location_id, updated_device)

    def remove_device(self, location_id: str, device_uuid: str) -> None:
        """Remove a device using the data manager"""
        self.data_manager.remove_device(location_id, device_uuid)

    def get_device_by_id(self, device_id: str) -> DeviceModel | None:
        """Return a device by its id"""
        return self.data_manager.get_device_by_id(device_id)

    def get_devices_by_location(self, location_id: str) -> list[DeviceModel]:
        """Return a list of devices by location"""
        return self.data_manager.get_devices_by_location(location_id)

    def handle_device_telemetry_data(self, device_id: str, telemetry_data: TelemetryModel) -> None:
        """ Handle telemetry data received from a device: the data is stored only if the device is registered """

        # Check that the telemetry data is valid
        if telemetry_data is None or not isinstance(telemetry_data, TelemetryModel):
            raise ValueError("Invalid Telemetry Data")

        # If the device is registered, store the telemetry data
        if self.data_manager.get_device_by_id(device_id) is not None:
            self.data_manager.add_device_telemetry_data(device_id, telemetry_data)
            print(f'Telemetry data received from device {device_id}')
        else:
            raise ValueError(f"Device {device_id} not registered")

    def get_telemetry_data_by_device_id(self, device_id: str) -> list[TelemetryModel] | None:
        """
        Get telemetry data by device id from data manager
        :param device_id: Device id associated with telemetry data
        :return: List of telemetry data
        """
        return self.data_manager.get_telemetry_data_by_device_id(device_id)

    def is_location_registered(self, location_id: str) -> bool:
        """Check if a location is registered"""
        return self.data_manager.is_location_registered(location_id)
