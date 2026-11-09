from json import JSONDecodeError
from flask import request, Response
from flask_restful import Resource
from application.core_manager import CoreManager
from communication.api.dto.location_entity_response import LocationEntityResponse
from communication.api.dto.location_update_request import LocationUpdateRequest
from application.model.location_model import LocationModel


class LocationResource(Resource):

    def __init__(self, **kwargs):
        self.core_manager: CoreManager = kwargs['core_manager']

    def get(self, location_id):
        """ Get a location by its UUID """

        if self.core_manager.is_location_registered(location_id):
            location = self.core_manager.get_location_by_id(location_id)

            # Iterate over the dictionary to build a serializable device id list
            device_id_list = []
            for device in location.device_dictionary.values():
                device_id_list.append(device.uuid)

            location_entity_response = LocationEntityResponse(location.uuid,
                                                              location.name,
                                                              location.latitude,
                                                              location.longitude,
                                                              device_id_list)
            return location_entity_response.__dict__, 200  # return data and 200 OK code
        else:
            return {'error': "Location Not Found !"}, 404

    def delete(self, location_id):
        """ Delete a location by its UUID """
        try:
            if self.core_manager.is_location_registered(location_id):
                self.core_manager.remove_location(location_id)
                return Response(status=204)
            else:
                return {'error': "Location UUID not found"}, 404
        except Exception as e:
            return {'error': "Generic Internal Server Error ! Reason: " + str(e)}, 500

    def put(self, location_id):
        """ Update a location by its UUID """

        try:
            if self.core_manager.is_location_registered(location_id):

                # The boolean flag force the parsing of POST data as JSON irrespective of the mimetype
                json_data = request.get_json(force=True)
                location_update_request = LocationUpdateRequest(**json_data)

                if self.core_manager.is_location_registered(location_update_request.uuid):
                    return {'error': "Location UUID not found exists"}, 404
                else:
                    updated_location_model = LocationModel(location_update_request.uuid,
                                                           location_update_request.name,
                                                           location_update_request.latitude,
                                                           location_update_request.longitude)
                    self.core_manager.update_location(updated_location_model)
                    return Response(status=204)
            else:
                return {'error': "Location UUID not found"}, 404
        except JSONDecodeError:
            return {'error': "Invalid JSON ! Check the request"}, 400
        except Exception as e:
            return {'error': "Generic Internal Server Error ! Reason: " + str(e)}, 500
