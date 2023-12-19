#!/usr/bin/env python3
from gemsModules.common.main_api_services import Service_Request, Service_Response
from gemsModules.common.main_api_notices import Notices

from gemsModules.delegator.tasks import (
    get_services_list,
    get_known_entities,
    get_subentity_services_list,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def Serve(request: Service_Request, entity=None) -> Service_Response:
    log.info("The Delegator ListServices server was called.")
    response = Service_Response()
    if request.typename != "ListServices":
        response.typename = request.typename
        response.outputs = {
            "message": "Incorrect typename sent to ListServices Servicer."
        }
        response.notices = Notices()
        response.notices.addDefaultNotice(
            Brief="InvalidInput", Messenger="ListServices Sevicer"
        )
    else:
        response.typename = "ListServices"
        if entity is None:
            response.outputs = get_services_list.execute()
        else:
            response.outputs = get_subentity_services_list.execute(entity)
    return response
