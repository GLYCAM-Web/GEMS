#!/usr/bin/env python3
import time
from pathlib import Path
from .api import Build_Selected_Positions_Request, Build_Selected_Positions_Response
from ..common_api import Position_Modification_Options
from .logic import execute
from gemsModules.systemoperations.instance_config import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)
ic = InstanceConfig()


def Serve(
    service: Build_Selected_Positions_Request,
) -> Build_Selected_Positions_Response:
    log.info(f"service: {service}")

    response = Build_Selected_Positions_Response()
    
    project_dir = Path(ic.get_filesystem_path("Glycomimetics")) / service.inputs.pUUID
    selected_position = service.inputs.Selected_Modification_Options
    if selected_position is None:
        # Check resources for a resourceRole: "Selected_Modification_Options"
        for r in service.inputs.resources:
            if r.resourceRole == "Selected_Modification_Options":
                log.debug("Found Selected_Modification_Opttions in resources...")
                selected_position = Position_Modification_Options(**r.get_payload())
                service.inputs.Selected_Modification_Options = selected_position
                break
        else:
            log.warning(f"No Position Selected, cannot run Glycomimetics/Build_Selected_Positions")
            response.notices.addNotice(
                Brief="No Position Selected",
                Scope="Build_Selected_Positions",
                Messenger="Glycomimetics",
                Type="Warning",
                Code="699",
                Message=f"No Position Selected, cannot run Glycomimetics"
            )     
            return response
        
    try:
        response.outputs = execute(service.inputs)
        
        ## TODO: we need a status service to check if the job is done - cannot delay response returns.
        # wait for out.txt to be created
        # time.sleep(2)
        # check if Segmentation fault in out.txt
        # out_txt = project_dir / "out.txt"
        # if out_txt.exists():
        #     with open(out_txt, "r") as f:
        #         out_txt_content = f.read()
        #         if "Segmentation fault" in out_txt_content:
        #             response.notices.addNotice(
        #                 Brief="Segmentation fault in out.txt",
        #                 Scope="Build_Selected_Positions",
        #                 Messenger="Glycomimetics",
        #                 Type="Error",
        #                 Code="701",
        #                 Message="Segmentation fault in out.txt"
        #             )
        #         else:
        #             response.notices.addNotice(
        #                 Brief="Glycomimetics ran successfully",
        #                 Scope="Build_Selected_Positions",
        #                 Messenger="Glycomimetics",
        #                 Type="Info",
        #                 Code="0",
        #                 Message="Glycomimetics ran successfully"
        #             )
        # else:
        #     response.notices.addNotice(
        #         Brief="No out.txt, Glycomimetics did not run",
        #         Scope="Build_Selected_Positions",
        #         Messenger="Glycomimetics",
        #         Type="Error",
        #         Code="702",
        #         Message=f"No {out_txt}, Glycomimetics did not run"
        #    )
        # just say it's running
        # TODO: Status check GM/Build/out.txt
        response.notices.addNotice(
            Brief="Glycomimetics is running, follow the out.log in the project directory for details",
            Scope="Build_Selected_Positions",
            Messenger="Glycomimetics",
            Type="Info",
            Code="600",
            Message="Glycomimetics is running"
        )
    except Exception as e:
        log.exception(f"Error running Glycomimetics: {e}")
        # append notice
        response.notices.addNotice(
            Brief="Error running Glycomimetics",
            Scope="Build_Selected_Positions",
            Messenger="Glycomimetics",
            Type="Error",
            Code="601",
            Message=f"Error running Glycomimetics: {e}",
        )
        
    return response
