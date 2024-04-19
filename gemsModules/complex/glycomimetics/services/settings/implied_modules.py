from typing import Dict, Callable

from gemsModules.common.services.error.implied_translator import (
    error_Implied_Translator,
)
from gemsModules.common.services.marco.implied_translator import (
    marco_Implied_Translator,
)
from gemsModules.common.services.status.implied_translator import (
    status_Implied_Translator,
)

from gemsModules.complex.glycomimetics.services.list_services.implied_translator import (
    list_services_Implied_Translator,
)
from gemsModules.complex.glycomimetics.services.Build.implied_translator import (
    Build_Implied_Translator,
)
from gemsModules.complex.glycomimetics.services.ProjectManagement.implied_translator import (
    ProjectManagement_Implied_Translator,
)
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)

implied_modules: Dict[str, Callable] = {
    "Error": error_Implied_Translator,
    "ListServices": list_services_Implied_Translator,
    "Marco": marco_Implied_Translator,
    "Status": status_Implied_Translator,
    "Build": Build_Implied_Translator,
    "ProjectManagement": ProjectManagement_Implied_Translator,
}
