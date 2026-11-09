# HTTP client creating a new Device in a Location through the RESTful API.
# From the project root run: uv run create-device [device_id] [location_id]

import sys
from typing import Any

import requests

from iot_monolithic_playground.tester.http.api_config import build_api_base_url

# Configuration variables
default_device_id = "test_device_1"
default_location_id = "l0001"


def main() -> None:

    device_id = sys.argv[1] if len(sys.argv) > 1 else default_device_id
    location_id = sys.argv[2] if len(sys.argv) > 2 else default_location_id
    api_url = f"{build_api_base_url()}/location/{location_id}/device"

    # Create Request Body as Python dictionary
    request_dictionary: dict[str, Any] = {
        "uuid": device_id,
        "name": f"Test Device {device_id}",
        "device_type": "device.default",
        "manufacturer": "ACME Inc",
        "software_version": "0.0.1beta",
        "latitude": 48.312321,
        "longitude": 10.433423211
    }

    # Send the POST Request with the body serialized as JSON (internally managed by the library)
    response = requests.post(api_url, json=request_dictionary)

    print(f"POST {api_url}")
    print(f"HTTP Response Code: {response.status_code} - Body: {response.content!r} "
          f"- Location Header: {response.headers.get('Location')}")


if __name__ == "__main__":
    main()
