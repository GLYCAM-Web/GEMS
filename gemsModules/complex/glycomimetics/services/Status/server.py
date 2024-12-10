#!/usr/bin/env python3
from pydantic import validate_arguments

from .api import Status_Request, Status_Response, Status_Inputs, Status_Outputs
from .logic import execute
from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


# Error
@validate_arguments
def Serve(service: Status_Request) -> Status_Response:
    log.info("Serve called")
    log.info(f"service: {service}")

    log.debug(f"service.inputs: {service.inputs}")

    # TODO: Pydantic should automatically do this...
    results, notices = execute(service.inputs)

    return Status_Response(outputs=results, notices=notices)
