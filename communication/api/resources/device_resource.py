from json import JSONDecodeError
from flask import request, Response
from flask_restful import Resource
from application.core_manager import CoreManager
from communication.api.dto.device_update_request import DeviceUpdateRequest
from application.model.device_model import DeviceModel


class DeviceResource(Resource):

    def __init__(self, **kwargs):
        self.core_manager: CoreManager = kwargs['core_manager']

    def get(self, location_id, device_id):
        """ Retrieve a specific device by its UUID """

        # Check if the provided Location Id in the path is correct
        if self.core_manager.is_location_registered(location_id):

            # Retrieve Location through its location_id
            target_location = self.core_manager.get_location_by_id(location_id)

            if device_id in target_location.device_dictionary:
                return target_location.device_dictionary[device_id].__dict__, 200  # return data and 200 OK code
            else:
                return {'error': "Device Not Found !"}, 404

        else:
            return {'error': "Location Not Found !"}, 404

    def delete(self, location_id, device_id):
        """ Delete a specific device by its UUID """

        try:

            # Check if the provided Location Id in the path is correct
            if self.core_manager.is_location_registered(location_id):

                # Retrieve Location through its location_id
                target_location = self.core_manager.get_location_by_id(location_id)

                if device_id in target_location.device_dictionary:
                    self.core_manager.remove_device(location_id, device_id)
                    return Response(status=204)
                else:
                    return {'error': "Device UUID not found"}, 404
            else:
                return {'error': "Location Not Found !"}, 404

        except Exception as e:
            return {'error': "Generic Internal Server Error ! Reason: " + str(e)}, 500

    def put(self, location_id, device_id):
        """ Update a specific device by its UUID """

        try:
            # Check if the provided Location Id in the path is correct
            if self.core_manager.is_location_registered(location_id):

                # Retrieve Location through its location_id
                target_location = self.core_manager.get_location_by_id(location_id)

                if device_id in target_location.device_dictionary:
                    # The boolean flag force the parsing of POST data as JSON irrespective of the mimetype
                    json_data = request.get_json(force=True)
                    device_update_request = DeviceUpdateRequest(**json_data)
                    if device_update_request.uuid != device_id:
                        return {'error': "UUID mismatch between body and resource"}, 400
                    else:

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
                else:
                    return {'error': "Device UUID not found"}, 404
            else:
                return {'error': "Location Not Found !"}, 404
        except JSONDecodeError:
            return {'error': "Invalid JSON ! Check the request"}, 400
        except Exception as e:
            return {'error': "Generic Internal Server Error ! Reason: " + str(e)}, 500
