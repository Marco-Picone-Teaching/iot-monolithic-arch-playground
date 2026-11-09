from typing import Any

from iot_monolithic_playground.config.config_loader import ConfigLoader

# The MQTT testers use the same broker (and optional credentials) of the MQTT Data Fetcher of the application
MQTT_CONFIG_FILE = "config/mqtt_fetcher_conf.yaml"


def load_broker_configuration() -> dict[str, Any]:
    """ Load the broker parameters (broker_ip, broker_port, username, password) from the fetcher configuration """
    return ConfigLoader.load(MQTT_CONFIG_FILE, {"broker_ip": "127.0.0.1", "broker_port": 1883,
                                                "username": None, "password": None})
