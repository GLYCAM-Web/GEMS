from typing import Dict, Callable

from gemsModules.common.services.error.manage_multiples import error_Multiples_Manager
from gemsModules.common.services.marco.manage_multiples import marco_Multiples_Manager

from gemsModules.complex.glycomimetics.services.Status.manage_multiples import Status_Multiples_Manager
from gemsModules.complex.glycomimetics.services.list_services.manage_multiples import (
    list_services_Multiples_Manager,
)
from gemsModules.complex.glycomimetics.services.Build_Selected_Positions.manage_multiples import (
    Build_Multiples_Manager,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)

duplicates_modules: Dict[str, Callable] = {
    "Error": error_Multiples_Manager,
    "ListServices": list_services_Multiples_Manager,
    "Marco": marco_Multiples_Manager,
    "Status": Status_Multiples_Manager,
    "Build_Selected_Positions": Build_Multiples_Manager,
}
