import threading
from pathlib import Path
from typing import Any

from flask import Flask, render_template
from werkzeug.serving import BaseWSGIServer, make_server

from iot_monolithic_playground.application.core_manager import CoreManager
from iot_monolithic_playground.config.config_loader import ConfigLoader

# Folder of the Presentation Layer templates: src/iot_monolithic_playground/presentation
TEMPLATE_DIR = Path(__file__).resolve().parents[2] / "presentation"


class WebServer:
    """
    Web Server of the Communication Layer: it renders the HTML templates of the Presentation Layer
    with the data provided by the Application Layer. The HTTP server runs in a dedicated thread.
    """

    # Default configuration, used for the parameters not defined in the configuration file
    DEFAULT_CONFIGURATION: dict[str, Any] = {
        "web": {
            "host": "0.0.0.0",
            "port": 7071
        }
    }

    def __init__(self, config_file: str, core_manager: CoreManager) -> None:

        # Core Manager of the Application Layer
        self.core_manager = core_manager

        # Read the configuration from the target configuration file
        self.configuration_dict = ConfigLoader.load(config_file, self.DEFAULT_CONFIGURATION)

        # HTTP server and its thread (created by start())
        self.http_server: BaseWSGIServer | None = None
        self.server_thread: threading.Thread | None = None

        # Create the Flask app using the templates of the Presentation Layer
        self.app = Flask(__name__, template_folder=str(TEMPLATE_DIR))

        # Add URL rules to the Flask app mapping the URL to the function
        self.app.add_url_rule('/locations', 'locations', self.locations)
        self.app.add_url_rule('/location/<string:location_id>/devices', 'devices', self.devices)
        self.app.add_url_rule('/location/<string:location_id>/device/<string:device_id>/telemetry', 'telemetry',
                              self.telemetry)

    def locations(self) -> str:
        """ Get all locations and render the locations.html template"""
        location_list = self.core_manager.get_all_locations()
        return render_template('locations.html', locations=location_list)

    def devices(self, location_id: str) -> Any:
        """ Get all devices for a specific location and render the devices.html template"""
        if not self.core_manager.is_location_registered(location_id):
            return f"Location {location_id} not found", 404
        device_list = self.core_manager.get_devices_by_location(location_id)
        return render_template('devices.html', devices=device_list, location_id=location_id)

    def telemetry(self, location_id: str, device_id: str) -> str:
        """ Get telemetry data for a specific device and render the telemetry.html template"""
        telemetry_data = self.core_manager.get_telemetry_data_by_device_id(device_id)
        return render_template('telemetry.html', telemetry_data=telemetry_data, location_id=location_id,
                               device_id=device_id)

    def start(self) -> None:
        """ Start the Web Server in a dedicated thread """

        host = self.configuration_dict['web']['host']
        port = self.configuration_dict['web']['port']

        # make_server() binds the socket immediately: an error (e.g., port already in use) is raised here
        self.http_server = make_server(host, port, self.app, threaded=True)
        self.server_thread = threading.Thread(target=self.http_server.serve_forever, name="web-server", daemon=True)
        self.server_thread.start()

        print(f"Web Server running on http://{host}:{port}/locations")

    def stop(self) -> None:
        """ Stop the Web Server and wait for its thread """
        if self.http_server is not None:
            self.http_server.shutdown()
        if self.server_thread is not None:
            self.server_thread.join()
        print("Web Server stopped")
