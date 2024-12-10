#!/usr/bin/env python3
from typing import Dict, Callable
from gemsModules.common.services.error.server import Serve as serve_error
from gemsModules.common.services.list_services.server import (
    Serve as serve_list_services,
)
from gemsModules.common.services.marco.server import Serve as serve_marco


from ..Build_Selected_Positions.server import Serve as serve_build
from ..ProjectManagement.server import Serve as serve_ProjectManagement
from ..Validate.server import Serve as serve_validate
from ..Evaluate.server import Serve as serve_evaluate
from ..Analyze.server import Serve as serve_analyze
from ..Status.server import Serve as serve_status

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)

service_modules: Dict[str, Callable] = {
    "Error": serve_error,
    "ListServices": serve_list_services,
    "Marco": serve_marco,
    "Status": serve_status,
    "Evaluate": serve_evaluate,
    "Validate": serve_validate,
    "ProjectManagement": serve_ProjectManagement,
    "Build_Selected_Positions": serve_build,
    "Analyze": serve_analyze,
}
