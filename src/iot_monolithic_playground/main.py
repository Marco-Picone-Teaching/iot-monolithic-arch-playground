# Entry point of the IoT Monolithic Application. From the project root run: uv run iot-monolith
#
# The monolith is a single process that creates the layers of the n-Tier architecture from the bottom to the top:
# Data Access Layer (DataManager) -> Application Layer (CoreManager) -> Communication Layer (RestApiServer,
# WebServer, MqttDataFetcher). The three modules of the Communication Layer run in parallel in dedicated threads.

import threading

from iot_monolithic_playground.application.core_manager import CoreManager
from iot_monolithic_playground.communication.api.rest_api_server import RestApiServer
from iot_monolithic_playground.communication.mqtt.mqtt_data_fetcher import MqttDataFetcher
from iot_monolithic_playground.communication.web.web_server import WebServer
from iot_monolithic_playground.data.data_manager import DataManager

# Configuration files (relative to the project root or to the working directory)
API_CONFIG_FILE = "config/api_conf.yaml"
WEB_CONFIG_FILE = "config/web_conf.yaml"
MQTT_CONFIG_FILE = "config/mqtt_fetcher_conf.yaml"


def main() -> None:

    # Data Access Layer: Data Manager initialization with some demo data
    data_manager = DataManager()
    data_manager.init_demo_data()

    # Application Layer: Core Manager with the Data Manager reference
    core_manager = CoreManager(data_manager)

    # Communication Layer: RESTful API Server, Web Server and MQTT Data Fetcher
    rest_api_server = RestApiServer(API_CONFIG_FILE, core_manager)
    web_server = WebServer(WEB_CONFIG_FILE, core_manager)
    mqtt_data_fetcher = MqttDataFetcher(MQTT_CONFIG_FILE, core_manager)

    # Start the modules of the Communication Layer, each one in its own thread
    rest_api_server.start()
    web_server.start()
    mqtt_data_fetcher.start()

    print("IoT Monolithic Application running (CTRL+C to stop)")

    try:
        # Keep the main thread alive while the modules are running
        threading.Event().wait()
    except KeyboardInterrupt:
        print("Stopping the IoT Monolithic Application ...")
    finally:
        mqtt_data_fetcher.stop()
        web_server.stop()
        rest_api_server.stop()


if __name__ == "__main__":
    main()
