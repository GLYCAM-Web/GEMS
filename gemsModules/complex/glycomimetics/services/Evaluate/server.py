#!/usr/bin/env python3
#from gemsModules.common.main_api_services import Service_Request, Service_Response
from .api import Evaluate_Request, Evaluate_Response
from .api import Evaluate_Inputs
from .logic import execute

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


def Serve(service: Evaluate_Request) -> Evaluate_Response:
    log.info("Serve called")
    log.info(f"service: {service}")
    log.debug(f"Eval service.inputs: {service.inputs}")
    response = Evaluate_Response()

    # Execute the service
    response.outputs = execute(service.inputs)

    return response
