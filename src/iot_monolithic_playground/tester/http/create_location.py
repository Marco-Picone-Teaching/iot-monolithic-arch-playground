# HTTP client creating a new Location through the RESTful API.
# From the project root run: uv run create-location [location_id]

import sys
from typing import Any

import requests

from iot_monolithic_playground.tester.http.api_config import build_api_base_url

# Configuration variables
default_location_id = "l0002"


def main() -> None:

    location_id = sys.argv[1] if len(sys.argv) > 1 else default_location_id
    api_url = build_api_base_url() + "/location"

    # Create Request Body as Python dictionary
    request_dictionary: dict[str, Any] = {
        "uuid": location_id,
        "name": "PythonTestBuilding",
        "latitude": 48.412321,
        "longitude": 10.533423211
    }

    # Send the POST Request with the body serialized as JSON (internally managed by the library)
    response = requests.post(api_url, json=request_dictionary)

    print(f"POST {api_url}")
    print(f"HTTP Response Code: {response.status_code} - Body: {response.content!r} "
          f"- Location Header: {response.headers.get('Location')}")


if __name__ == "__main__":
    main()
