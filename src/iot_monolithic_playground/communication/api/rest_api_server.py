import threading
from typing import Any

from flask import Flask
from flask_restful import Api
from werkzeug.serving import BaseWSGIServer, make_server

from iot_monolithic_playground.application.core_manager import CoreManager
from iot_monolithic_playground.communication.api.resources.device_resource import DeviceResource
from iot_monolithic_playground.communication.api.resources.devices_resource import DevicesResource
from iot_monolithic_playground.communication.api.resources.location_resource import LocationResource
from iot_monolithic_playground.communication.api.resources.locations_resource import LocationsResource
from iot_monolithic_playground.config.config_loader import ConfigLoader


class RestApiServer:
    """
    RESTful API Server designed to manage the Inventory of IoT Devices.
    The HTTP server runs in a dedicated thread, so it can be executed together with the other modules of the monolith.
    """

    # Default configuration, used for the parameters not defined in the configuration file
    DEFAULT_CONFIGURATION: dict[str, Any] = {
        "rest": {
            "api_prefix": "/api/iot/inventory",
            "host": "0.0.0.0",
            "port": 7070
        }
    }

    def __init__(self, config_file: str, core_manager: CoreManager) -> None:

        # Core Manager of the Application Layer (the only layer the Communication Layer interacts with)
        self.core_manager = core_manager

        # Read the configuration from the target configuration file
        self.configuration_dict = ConfigLoader.load(config_file, self.DEFAULT_CONFIGURATION)

        # HTTP server and its thread (created by start())
        self.http_server: BaseWSGIServer | None = None
        self.server_thread: threading.Thread | None = None

        # Initialize the Flask application and the REST API
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.init_rest_api()

    def init_rest_api(self) -> None:
        """ Initialize the REST API with resources and endpoints """

        api_prefix = self.configuration_dict['rest']['api_prefix']
        resource_kwargs = {'core_manager': self.core_manager}

        self.api.add_resource(LocationsResource, api_prefix + '/location',
                              resource_class_kwargs=resource_kwargs,
                              endpoint="locations",
                              methods=['GET', 'POST'])

        self.api.add_resource(LocationResource, api_prefix + '/location/<string:location_id>',
                              resource_class_kwargs=resource_kwargs,
                              endpoint='location',
                              methods=['GET', 'PUT', 'DELETE'])

        self.api.add_resource(DevicesResource, api_prefix + '/location/<string:location_id>/device',
                              resource_class_kwargs=resource_kwargs,
                              endpoint="devices",
                              methods=['GET', 'POST'])

        self.api.add_resource(DeviceResource, api_prefix + '/location/<string:location_id>/device/<string:device_id>',
                              resource_class_kwargs=resource_kwargs,
                              endpoint='device',
                              methods=['GET', 'PUT', 'DELETE'])

    def start(self) -> None:
        """ Start the REST API Server in a dedicated thread """

        host = self.configuration_dict['rest']['host']
        port = self.configuration_dict['rest']['port']

        # make_server() binds the socket immediately: an error (e.g., port already in use) is raised here
        self.http_server = make_server(host, port, self.app, threaded=True)
        self.server_thread = threading.Thread(target=self.http_server.serve_forever, name="rest-api-server", daemon=True)
        self.server_thread.start()

        print(f"RESTful API Server running on http://{host}:{port}{self.configuration_dict['rest']['api_prefix']}")

    def stop(self) -> None:
        """ Stop the REST API Server and wait for its thread """
        if self.http_server is not None:
            self.http_server.shutdown()
        if self.server_thread is not None:
            self.server_thread.join()
        print("RESTful API Server stopped")
