#!/usr/bin/env python3
import os
from pathlib import Path
import sys
from typing import Protocol, Dict, Optional
from pydantic import BaseModel, validate_arguments

from gemsModules.common.main_api_notices import Notices
from gemsModules.systemoperations.instance_config import InstanceConfig
from gemsModules.logging.logger import Set_Up_Logging

from .api import Evaluate_Inputs, Evaluate_Outputs
from ..common_api import Modification_Position

from ...tasks import evaluate_wrapper

log = Set_Up_Logging(__name__)


@validate_arguments
def execute(inputs: Evaluate_Inputs) -> tuple[Evaluate_Outputs, Notices]:
    log.debug(f"serviceInputs: {inputs}")
    service_outputs = Evaluate_Outputs()
    service_notices = Notices()

    complex_pdb_resource = None
    for resource in inputs.resources:
        if resource.resourceRole == "Complex":
            complex_pdb_resource = resource
            break

    if not complex_pdb_resource:
        # Append a notice, we can do nothing else.
        service_notices.addNotice(
            Brief="No Complex PDB Resource",
            Scope="Service",
            Messenger="Glycomimetics",
            Type="Error",
            Code="601",
            Message="No Complex PDB was provided to Glycomimetics, nothing to do.",
        )
    else:
        # Evaluation
        if complex_pdb_resource.locationType != "filesystem-path-unix":
            service_notices.addNotice(
                Brief="current Complex PDB Resource Location type not supported",
                Scope="Service",
                Messenger="Glycomimetics",
                Type="Error",
                Code="602",
                Message="Complex PDB Resource must be a filesystem path.",
            )
        else:
            pdb_fpath = complex_pdb_resource.payload

            if Path(pdb_fpath).exists():
                working_dir = str(Path(pdb_fpath).parent)

                log.debug(
                    f"Complex PDB file found: {pdb_fpath}, working_dir: {working_dir}"
                )
                try:
                    # To ensure various output files are written to the correct directory.
                    parent_dir = str(Path(pdb_fpath).parent)
                    pdb_filename = Path(pdb_fpath).name
                    
                    condensed_sequences, available_positions = evaluate_wrapper.execute(parent_dir, pdb_filename)
                    # For now, we are only returning the first condensed sequence.
                    service_outputs.Condensed_Sequence = condensed_sequences[0]
                    service_outputs.Available_Modification_Options.extend(available_positions)
                    
                    log.debug(f"Got {len(condensed_sequences)} condensed sequences. Note: only returning the first.")
                    log.debug(f"Condensed_Sequence: {service_outputs.Condensed_Sequence}")
                    log.debug(
                        f"Available_Modification_Options: {service_outputs.Available_Modification_Options}"
                    )
                except Exception as e:
                    log.error(f"Error caught during Evaluation: {e}")
                    service_notices.addNotice(
                        Brief="Error during Evaluation",
                        Scope="Service",
                        Messenger="Glycomimetics",
                        Type="Error",
                        Code="603",
                        Message=f"Error during Evaluation: {e}",
                    )
                    
                # TODO: swig wrap or recover results from evaluation.log
                with open(os.path.join(parent_dir, "evaluation.log")) as f:
                    log.debug(f"evaluation.log contents:")
                    successful = False
                    # Pdb2glycam matching successful. scan for this then log all lines after it
                    while True:
                        line = f.readline()
                        if "Pdb2glycam matching successful" in line:
                            successful = True
                            break
                        if line == "":
                            break
                        
                    if successful:
                        for line in f:
                            log.debug(line.strip())
                    else:
                        log.debug("Pdb2glycam matching unsuccessful, evaluation failed.")
                        service_notices.addNotice(
                            Brief="Pdb2glycam matching unsuccessful",
                            Scope="Service",
                            Messenger="Glycomimetics",
                            Type="Error",
                            Code="604",
                            Message="Pdb2glycam matching unsuccessful, evaluation failed.",
                        )
            else:
                log.debug(f"Complex PDB file not found: {pdb_fpath}")

    if not len(service_notices):
        service_notices.addNotice(
            Brief="Evaluation Successful",
            Scope="Service",
            Messenger="Glycomimetics",
            Type="Info",
            Code="600",
            Message="Evaluation Successful",
        )

    log.debug(f"service_outputs: {service_outputs}")
    log.debug(f"service_notices: {service_notices}")
    return service_outputs, service_notices
