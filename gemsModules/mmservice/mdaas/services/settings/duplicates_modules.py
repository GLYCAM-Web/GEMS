from typing import Dict, Callable

from gemsModules.common.services.error.manage_multiples import error_Multiples_Manager
from gemsModules.common.services.marco.manage_multiples import marco_Multiples_Manager
from gemsModules.common.services.status.manage_multiples import status_Multiples_Manager
from gemsModules.delegator.services.list_services.manage_multiples import (
    list_services_Multiples_Manager,
)

from gemsModules.mmservice.mdaas.services.run_md.manage_multiples import (
    run_md_Multiples_Manager,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)

duplicates_modules: Dict[str, Callable] = {
    "Error": error_Multiples_Manager,
    "ListServices": list_services_Multiples_Manager,
    "Marco": marco_Multiples_Manager,
    "Status": status_Multiples_Manager,
    "RunMD": run_md_Multiples_Manager,
}
