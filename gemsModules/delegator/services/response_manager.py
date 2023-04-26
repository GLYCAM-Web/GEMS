#!/usr/bin/env python3

from gemsModules.common.services.response_manager import Response_Manager
from gemsModules.common.main_api_notices import Notices

from gemsModules.delegator.main_api import Delegator_Entity

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


class delegator_Response_Manager(Response_Manager):

    def generate_response_entity(self):
        self.response_entity = Delegator_Entity(type="Delegator")
        self.response_entity.notices = Notices()
        request_aaop_list=self.aaop_tree_pair.input_tree.make_linear_list()
        response_aaop_list=self.aaop_tree_pair.output_tree.make_linear_list()
        log.debug("the_request_aaop_list is: ")
        log.debug(request_aaop_list)
        log.debug("the_response_aaop_list is: ")
        log.debug(response_aaop_list)
        for aaop in request_aaop_list:
            this_service = aaop.The_AAO.copy(deep=True)
            this_service.myUuid = aaop.ID_String
            self.response_entity.services.add_service(key_string=aaop.Dictionary_Name, service=this_service)
        for aaop in response_aaop_list: 
            this_response = aaop.The_AAO.copy(deep=True)
            this_response.myUuid = aaop.ID_String
            this_response.notices = Notices()
            self.response_entity.responses.add_response(key_string=aaop.Dictionary_Name, response=this_response)

        log.debug("the response entity is: ")
        log.debug(self.response_entity.json(indent=2))

        return self.response_entity