import uuid
from gemsModules.common.main_api_resources import Resource
from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.workflow_manager import Workflow_Manager
from gemsModules.common.code_utils import Annotated_List, resolve_dependency_list

from gemsModules.mmservice.mdaas.services.run_md.run_md_api import (
    run_md_Request,
)
from gemsModules.mmservice.mdaas.services.ProjectManagement.api import (
    ProjectManagement_Request,
)
from gemsModules.mmservice.mdaas.services.Evaluate.api import (
    Evaluate_Request,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


# TODO: To services.settings... ?
EVAL_DEPS = Annotated_List([], ordered=True)
PRMN_DEPS = Annotated_List(EVAL_DEPS + ["Evaluate"], ordered=True)
RNMD_DEPS = Annotated_List(PRMN_DEPS + ["ProjectManagement"], ordered=True)

# TODO: To services.settings... ?
Service_Dependencies = {
    "Evaluate": EVAL_DEPS,
    "ProjectManagement": PRMN_DEPS,
    "RunMD": RNMD_DEPS
}

# TODO: work_flows style or workflow_manager style?
class mdaas_Workflow_Manager(Workflow_Manager):
    def get_linear_workflow_list(self) -> list[str]:
        return ["ProjectManagement", "RunMD"]

    def process(self, aaop_list):
        """This function takes a list of AAOPs and returns a list of AAOPs in the order they should be executed."""
        log.debug("\tthe service dependencies are: %s", Service_Dependencies)

        ordered = Annotated_List(ordered=True)
        unordered = aaop_list.copy()
        log.debug("\tthe unordered aaop request list is: %s", unordered)

        # Use AAO_type and Service_Dependencies dict to determine AAOP execution order.
        while len(unordered) > 0:
            # Get the next aaop
            current_aaop = unordered.pop(0)
            log.debug(f"Resolving dependencies for {current_aaop.AAO_Type}")

            # TODO: resolve/unify these_deps against prior deps
            these_deps = resolve_dependency_list(
                current_aaop.AAO_Type, Service_Dependencies
            )
            log.debug(
                "\tthe ordered dependencies for %s are: %s",
                current_aaop.AAO_Type,
                these_deps,
            )

            for new_dep in these_deps:
                log.debug("Resolving dependency %s", new_dep)
                # TODO: You can probably put the Service classes in the dependency dict 
                # itself and construct the class directly.
                aao_cls = globals()[f"{new_dep}_Request"]
                
                new_aaop = AAOP(
                    AAO_Type=new_dep,
                    The_AAO=aao_cls(),
                    ID_String=uuid.uuid4(),
                    Dictionary_Name=f"{new_dep}_Dep_Request",
                )
                new_aaop.set_requester(current_aaop)

                log.debug(
                    "Adding dependency %s to aaop list before %s",
                    new_aaop,
                    current_aaop,
                )                
                ordered.append(new_aaop)

            # Add this aaop after we're finished with its deps
            ordered.append(current_aaop)
        return ordered

