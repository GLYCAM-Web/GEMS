#!/usr/bin/env python3
import os
from typing import Protocol, Dict, Optional
from pydantic import BaseModel

from gemsModules.structurefile.PDBFile.tasks import prepare_pdb
from gemsModules.structurefile.PDBFile.services.ProjectManagement.api import (
    ProjectManagement_Inputs,
    ProjectManagement_Outputs,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def execute(inputs: ProjectManagement_Inputs) -> ProjectManagement_Outputs:
    """Executes the service."""
    log.debug(f"serviceInputs: {inputs}")
    service_outputs = ProjectManagement_Outputs()

    log.debug("Creating project directory: " + str(inputs.projectDir))
    os.makedirs(inputs.projectDir, exist_ok=True)

    log.debug("ProjectManagement Resource list: " + str(inputs.resources))
    for resource in inputs.resources:
        log.debug(f"Copying resource: {resource} to project directory.")
        file_resource = resource.copy_to(inputs.projectDir)
        service_outputs.resources.add_resource(file_resource)

    return service_outputs
