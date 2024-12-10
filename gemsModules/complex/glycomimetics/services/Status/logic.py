#!/usr/bin/env python3
from typing import Protocol, Dict, Optional
from pydantic import BaseModel, validate_arguments

from gemsModules.common.main_api_notices import Notices
from gemsModules.systemoperations.instance_config import InstanceConfig
from gemsModules.logging.logger import Set_Up_Logging

from .api import Status_Inputs, Status_Outputs


log = Set_Up_Logging(__name__)


def execute(inputs: Status_Inputs) -> Status_Outputs:
    log.debug(f"Status resources at servicing: {inputs}")
    service_outputs = Status_Outputs()
    service_notices = Notices()

    hasComplexResource = False
    for resource in inputs.resources:
        if resource.resourceRole == "Complex":
            hasComplexResource = True

    if not hasComplexResource:
        service_notices.addNotice(
            Brief="No Complex PDB Resource",
            Scope="Service",
            Messenger="Glycomimetics",
            Type="Error",
            Code="600",
            Message="No Complex PDB was provided to Glycomimetics.",
        )
        service_outputs.isValid = False
    else:
        # TODO: Use PDB Preprocessor or similar to check PDB
        service_outputs.isValid = True

    log.debug(f"service_outputs: {service_outputs}")
    return service_outputs, service_notices
