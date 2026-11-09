from json import JSONDecodeError
from typing import Any

from flask import request, Response
from flask_restful import Resource

from iot_monolithic_playground.application.core_manager import CoreManager
from iot_monolithic_playground.application.model.device_model import DeviceModel
from iot_monolithic_playground.communication.api.dto.device_update_request import DeviceUpdateRequest


class DeviceResource(Resource):
    """ Single Device of a Location identified by its UUID: read (GET), update (PUT) and delete (DELETE) """

    def __init__(self, **kwargs: Any) -> None:
        self.core_manager: CoreManager = kwargs['core_manager']

    def get(self, location_id: str, device_id: str) -> Any:
        """ Retrieve a specific device by its UUID """

        target_location = self.core_manager.get_location_by_id(location_id)
        if target_location is None:
            return {'error': "Location Not Found !"}, 404

        if device_id in target_location.device_dictionary:
            return target_location.device_dictionary[device_id].__dict__, 200
        else:
            return {'error': "Device Not Found !"}, 404

    def delete(self, location_id: str, device_id: str) -> Any:
        """ Delete a specific device by its UUID """

        try:
            target_location = self.core_manager.get_location_by_id(location_id)
            if target_location is None:
                return {'error': "Location Not Found !"}, 404

            if device_id in target_location.device_dictionary:
                self.core_manager.remove_device(location_id, device_id)
                return Response(status=204)
            else:
                return {'error': "Device UUID not found"}, 404

        except Exception as e:
            return {'error': "Generic Internal Server Error ! Reason: " + str(e)}, 500

    def put(self, location_id: str, device_id: str) -> Any:
        """ Update a specific device by its UUID """

        try:
            target_location = self.core_manager.get_location_by_id(location_id)
            if target_location is None:
                return {'error': "Location Not Found !"}, 404

            if device_id not in target_location.device_dictionary:
                return {'error': "Device UUID not found"}, 404

            # The boolean flag force the parsing of PUT data as JSON irrespective of the mimetype
            json_data = request.get_json(force=True)
            device_update_request = DeviceUpdateRequest(**json_data)

            # The UUID in the body must match the UUID of the resource
            if device_update_request.uuid != device_id:
                return {'error': "UUID mismatch between body and resource"}, 400

            update_device_model = DeviceModel(device_id,
                                              device_update_request.name,
                                              location_id,
                                              device_update_request.type,
                                              device_update_request.manufacturer,
                                              device_update_request.software_version,
                                              device_update_request.latitude,
                                              device_update_request.longitude)

            self.core_manager.update_device(location_id, update_device_model)
            return Response(status=204)
        except (JSONDecodeError, TypeError):
            return {'error': "Invalid JSON ! Check the request"}, 400
        except Exception as e:
            return {'error': "Generic Internal Server Error ! Reason: " + str(e)}, 500
