import json
from typing import Any

import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.reasoncodes import ReasonCode

from iot_monolithic_playground.application.core_manager import CoreManager
from iot_monolithic_playground.application.model.telemetry_model import TelemetryModel
from iot_monolithic_playground.communication.mqtt.dto.telemetry_message import TelemetryMessage
from iot_monolithic_playground.config.config_loader import ConfigLoader


class MqttDataFetcher:
    """
    MQTT Data Fetcher of the Communication Layer: it subscribes to the telemetry topic of the devices and forwards
    the received data to the Application Layer.
    The Paho network loop runs in its own thread (loop_start), so the fetcher does not block the other modules.
    """

    # Default configuration, used for the parameters not defined in the configuration file
    DEFAULT_CONFIGURATION: dict[str, Any] = {
        "broker_ip": "127.0.0.1",
        "broker_port": 1883,
        "client_id": "iot-monolithic-playground-fetcher",
        "target_telemetry_topic": "device/+/temperature",
        "username": None,
        "password": None
    }

    def __init__(self, config_file: str, core_manager: CoreManager) -> None:

        # Core Manager of the Application Layer
        self.core_manager = core_manager

        # Read the configuration from the target configuration file
        self.configuration_dict = ConfigLoader.load(config_file, self.DEFAULT_CONFIGURATION)

        # MQTT Broker Configuration
        self.mqtt_broker_host: str = self.configuration_dict["broker_ip"]
        self.mqtt_broker_port: int = self.configuration_dict["broker_port"]
        self.mqtt_topic: str = self.configuration_dict["target_telemetry_topic"]
        self.mqtt_username: str | None = self.configuration_dict["username"]
        self.mqtt_password: str | None = self.configuration_dict["password"]

        # Create the MQTT client (Paho 2.x requires the Callback API version)
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, self.configuration_dict["client_id"])
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    def on_connect(self, client: mqtt.Client, userdata: Any, flags: mqtt.ConnectFlags,
                   reason_code: ReasonCode, properties: Properties | None) -> None:
        """ Callback for the CONNACK response of the broker: subscribe only after a successful connection.
        It is called again at each automatic reconnection, renewing the subscription """

        if reason_code.is_failure:
            print(f"MQTT Data Fetcher - Connection refused: {reason_code}")
            return

        print(f"MQTT Data Fetcher - Connected to {self.mqtt_broker_host}:{self.mqtt_broker_port} ({reason_code})")
        client.subscribe(self.mqtt_topic)
        print(f"MQTT Data Fetcher - Subscribed to topic: {self.mqtt_topic}")

    def on_disconnect(self, client: mqtt.Client, userdata: Any, flags: mqtt.DisconnectFlags,
                      reason_code: ReasonCode, properties: Properties | None) -> None:
        """ Callback for the disconnection from the broker (Paho reconnects automatically) """
        print(f"MQTT Data Fetcher - Disconnected: {reason_code}")

    def on_message(self, client: mqtt.Client, userdata: Any, message: mqtt.MQTTMessage) -> None:
        """ Callback for the received messages: deserialize the telemetry and forward it to the Application Layer """

        if not mqtt.topic_matches_sub(self.mqtt_topic, message.topic):
            return

        try:
            payload = message.payload.decode("utf-8")

            # Extract the device ID from the topic (device/<device_id>/temperature)
            device_id = message.topic.split('/')[1]

            # Deserialize the payload into the TelemetryMessage DTO
            telemetry_message = TelemetryMessage(**json.loads(payload))
            print(f"MQTT Data Fetcher - Received message from device {device_id}: {payload}")

            # Convert the DTO into the domain model of the Application Layer and handle it
            telemetry_model = TelemetryModel(telemetry_message.timestamp,
                                             telemetry_message.data_type,
                                             telemetry_message.value)
            self.core_manager.handle_device_telemetry_data(device_id, telemetry_model)

        except Exception as e:
            print(f"MQTT Data Fetcher - Error processing message on {message.topic}: {e}")

    def start(self) -> None:
        """ Connect to the MQTT Broker and start the Paho network loop in a background thread """

        # Set the credentials only if they are configured
        if self.mqtt_username and self.mqtt_password:
            print("MQTT Data Fetcher - Setting username and password ...")
            self.client.username_pw_set(self.mqtt_username, self.mqtt_password)

        # connect_async() does not block: the connection (and the retries if the broker is not available yet)
        # are managed by the network loop started by loop_start()
        print(f"MQTT Data Fetcher - Connecting to {self.mqtt_broker_host}:{self.mqtt_broker_port} ...")
        self.client.connect_async(self.mqtt_broker_host, self.mqtt_broker_port, 60)
        self.client.loop_start()

    def stop(self) -> None:
        """ Disconnect from the MQTT Broker and stop the network loop """
        self.client.disconnect()
        self.client.loop_stop()
        print("MQTT Data Fetcher stopped")
