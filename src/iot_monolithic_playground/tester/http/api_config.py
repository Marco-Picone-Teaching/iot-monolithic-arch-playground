from iot_monolithic_playground.config.config_loader import ConfigLoader

# The HTTP testers read the API prefix and port from the configuration of the RESTful API Server
API_CONFIG_FILE = "config/api_conf.yaml"

# Host of the RESTful API Server targeted by the testers
API_HOST = "127.0.0.1"


def build_api_base_url() -> str:
    """ Build the base URL of the RESTful API, e.g., http://127.0.0.1:7070/api/iot/inventory """
    configuration = ConfigLoader.load(API_CONFIG_FILE, {"rest": {"api_prefix": "/api/iot/inventory", "port": 7070}})
    return f"http://{API_HOST}:{configuration['rest']['port']}{configuration['rest']['api_prefix']}"
