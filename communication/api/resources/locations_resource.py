from json import JSONDecodeError
from flask import request, Response
from flask_restful import Resource

from application.core_manager import CoreManager
from communication.api.dto.location_entity_response import LocationEntityResponse
from communication.api.dto.location_creation_request import LocationCreationRequest
from application.model.location_model import LocationModel


class LocationsResource(Resource):

    def __init__(self, **kwargs):
        self.core_manager: CoreManager = kwargs['core_manager']

    def post(self):
        """Create a new location"""
        try:
            # The boolean flag force the parsing of POST data as JSON irrespective of the mimetype
            json_data = request.get_json(force=True)
            location_creation_request = LocationCreationRequest(**json_data)
            if self.core_manager.is_location_registered(location_creation_request.uuid):
                return {'error': "Location UUID already exists"}, 409  # return data and 200 OK code
            else:
                new_location_model = LocationModel(location_creation_request.uuid,
                                                   location_creation_request.name,
                                                   location_creation_request.latitude,
                                                   location_creation_request.longitude)
                self.core_manager.add_location(new_location_model)
                return Response(status=201, headers={"Location": request.url+"/"+new_location_model.uuid})  # Force the No-Content Response
        except JSONDecodeError:
            return {'error': "Invalid JSON ! Check the request"}, 400
        except Exception as e:
            return {'error': "Generic Internal Server Error ! Reason: " + str(e)}, 500

    def get(self):

        # Iterate over the dictionary to build a serializable device list
        result_location_list = []

        for location in self.core_manager.get_all_locations():

            # Iterate over the dictionary to build a serializable device id list
            device_id_list = []
            for device in location.device_dictionary.values():
                device_id_list.append(device.uuid)

            location_entity_response = LocationEntityResponse(location.uuid,
                                                              location.name,
                                                              location.latitude,
                                                              location.longitude,
                                                              device_id_list)

            result_location_list.append(location_entity_response.__dict__)

        return result_location_list, 200  # return data and 200 OK code