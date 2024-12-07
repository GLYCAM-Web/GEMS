from gemsModules.common.code_utils import GemsStrEnum

from gemsModules.common.services.settings.known_available import (
    Module_Available_Services as Common_Available_Services,
)
from gemsModules.mmservice.each_service.known_available import (
    Mmservice_Allowed_File_Formats,
)


from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Module_Available_Services(GemsStrEnum):
    # TODO: Rename key to match service name
    AmberMDPrep = "AmberMDPrep"
    ProjectManagement = "ProjectManagement"


Available_Services = GemsStrEnum(
    "Available_Services",
    [(avail.name, avail.value) for avail in Common_Available_Services]
    + [(avail.name, avail.value) for avail in Module_Available_Services],
)


class Module_Allowed_File_Formats(GemsStrEnum):
    amber_pdb = "pdb"


Allowed_File_Formats = GemsStrEnum(
    "Allowed_File_Formats",
    [(avail.name, avail.value) for avail in Mmservice_Allowed_File_Formats]
    + [(avail.name, avail.value) for avail in Module_Allowed_File_Formats],
)
