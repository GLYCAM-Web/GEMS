#!/usr/bin/env python3
from typing import Protocol, Dict, Optional
from pydantic import BaseModel, validate_arguments
from pathlib import Path

from gemsModules.common.main_api_notices import Notices
from gemsModules.systemoperations.instance_config import InstanceConfig
from gemsModules.logging.logger import Set_Up_Logging
from gemsModules.systemoperations.instance_config import InstanceConfig

from .api import Status_Inputs, Status_Outputs


log = Set_Up_Logging(__name__)

GLYCOMIMETICS_PROJECTS_ROOT = InstanceConfig().get_filesystem_path("Glycomimetics")


def execute(inputs: Status_Inputs) -> Status_Outputs:
    log.debug(f"Status resources at servicing: {inputs}")
    service_outputs = Status_Outputs()
    service_notices = Notices()

    # Check if the project exists
    project_path = Path(GLYCOMIMETICS_PROJECTS_ROOT, inputs.pUUID)
    if not project_path.exists():
        service_outputs.status = "NotFound"
        service_outputs.details = f"Project not found at {project_path}"
        return service_outputs, service_notices
        
    main_status_txt = project_path / "status.txt"
    
    # check for errors during evaluation
    evaluate_err = project_path / "evaluate.err"
    evaluation_log = project_path / "evaluation.log"
    
    non_empty_evaluate_err = evaluate_err.exists() and evaluate_err.stat().st_size > 0
    contains_success_str = False
    with open(evaluation_log, "r") as f:
        for line in f:
            if "Pdb2glycam matching successful." in line:
                contains_success_str = True
                break
            
    # if the main status doesn't exist, it might not be a Build project, look for errors during evaluation:
    if not main_status_txt.exists():
        # if evaluate_err non-empty, then the project failed during evaluation
        if non_empty_evaluate_err or not contains_success_str:
            service_outputs.status = "Failure"
            service_outputs.details = "Project failed during evaluation"
            return service_outputs, service_notices
        else:
            service_outputs.status = "Success"
            service_outputs.details = "Project successfully evaluated"
            return service_outputs, service_notices
    else:
        # if it exists, the last line of this file becomes the status details, if we get to
        # "Simulations completed." then it is a success
        with open(main_status_txt, "r") as f:
            for line in f:
                if "Simulations completed." in line:
                    service_outputs.status = "Success"
                    service_outputs.details = line
                    return service_outputs, service_notices
                elif "error" in line.lower():
                    service_outputs.status = "Failure"
                    service_outputs.details = line
                    return service_outputs, service_notices

    return service_outputs, service_notices
