import os
from pathlib import Path

from gemsModules.systemoperations.instance_config import InstanceConfig
from gemsModules.logging.logger import Set_Up_Logging

from .api import Build_Inputs, Build_Outputs
from ...tasks import create_gm_input_file, run_all_glyco, create_system_info_file


log = Set_Up_Logging(__name__)

ic = InstanceConfig()
# https://github.com/GLYCAM-Web/glycomimeticsWebtool/tree/main/internal
# TODO: Manage GlycoWebtool path with IC
GlycoWebtool_path = Path("/programs/glycomimeticsWebtool")


def execute(inputs: Build_Inputs) -> Build_Outputs:
    log.debug("Executing Build_Selected_Positions")
    service_outputs = Build_Outputs(pUUID=inputs.pUUID)

    # Normally the Project builds this path. TODO: better helper 
    project_dir = Path(ic.get_filesystem_path(app="Glycomimetics")) / inputs.pUUID
    if not project_dir.exists():
        log.debug(f"Warning: Project directory {project_dir} does not exist at time of Build_Selected_Positions.")
        raise RuntimeError("No project directory found, cannot run Glycomimetics/Build_Selected_Positions")
    else:
        # TODO: Move file creation to ProjectManagement service?
        # log.debug("Copying scripts")
        # # Note, we do not execute the copies, they are only for reference at this moment.
        # # check glyco exists
        # if not GlycoWebtool_path.exists():
        #     log.warning(f"Warning: GlycoWebtool path {GlycoWebtool_path} does not exist. Cannot run Glycomimetics.")
        # else:
        #     os.system(f"cp -r {GlycoWebtool_path}/scripts {project_dir}")
    
        # Create the input.txt for the Glycomimetics service.
        # Note: We only allow one Selected Position at a time in the API for now.
        log.debug("Creating Glycomimetics Run_ALL input.txt")
        create_gm_input_file.execute(inputs.Selected_Modification_Options.Position, project_dir, GlycoWebtool_path)
        
        # Create the systemInfo.txt
        log.debug("Creating systemInfo.txt")
        create_system_info_file.execute(project_dir, GlycoWebtool_path)
    
        # Run glycomimetics
        log.debug("Running Glycomimetics now...")
        try:
            run_all_glyco.execute(inputs.pUUID, project_dir, GlycoWebtool_path)
        except Exception as e:
            log.exception(f"Error running Glycomimetics: {e}")
            service_outputs.notices.addNotice(
            Brief="Glycomimetics RUN_ALL Error",
            Scope="Build_Selected_Positions",
            Messenger="Glycomimetics",
            Type="Error",
            Code="603",
            Message=f"Error running Glycomimetics RUN_ALL: {e}",
        ) 
    service_outputs.projectDir = str(project_dir)
    
    return service_outputs
