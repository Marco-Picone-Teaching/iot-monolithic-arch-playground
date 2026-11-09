import requests

import requests

LOCATION_ID = "l0001"

# Target API URL
api_url = "http://127.0.0.1:7070/api/iot/inventory/location/" + LOCATION_ID + "/device"

# Define Create Request Body as Python dictionary
request_dictionary = {
    "uuid": "test_device_1",
    "name": "Test Device 1",
    "device_type": "device.default",
    "manufacturer": "ACME Inc",
    "software_version": "0.0.1beta",
    "latitude": 48.312321,
    "longitude": 10.433423211
}

# Send the POST Request with the body serialized as Json (Internally managed by the library)
response = requests.post(api_url, json=request_dictionary)

location_header = response.headers["Location"]

print(f'HTTP Response Code: {response.status_code} - Buffer Body: {response.content} - Location Header: {location_header}')