from gemsModules.common.code_utils import GemsStrEnum

from gemsModules.common.services.settings.known_available import (
    Module_Available_Services as Common_Available_Services,
)

from gemsModules.complex.settings import Complex_Allowed_File_Formats

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Module_Available_Services(GemsStrEnum):
    Validate = "Validate"
    Evaluate = "Evaluate"
    ProjectManagement = "ProjectManagement"
    Build_Selected_Positions = "Build_Selected_Positions"
    Analyze = "Analyze"
    Status = "Status"


Available_Services = GemsStrEnum(
    "Available_Services",
    [(avail.name, avail.value) for avail in Common_Available_Services]
    + [(avail.name, avail.value) for avail in Module_Available_Services],
)


class Module_Allowed_File_Formats(GemsStrEnum):
    amber_parm7 = "amber_parm7"
    amber_rst7 = "amber_rst7"


Allowed_File_Formats = GemsStrEnum(
    "Allowed_File_Formats",
    [(avail.name, avail.value) for avail in Complex_Allowed_File_Formats]
    + [(avail.name, avail.value) for avail in Module_Allowed_File_Formats],
)


def testme():
    """Ensure that the settings info is complete.
    >>> testme()
    ['Error', 'Marco', 'Status', 'ListServices', 'RunMD']
    ['PDB', 'mmCIF', 'Mol2', 'xyz', 'amber_parm7', 'amber_rst7']

    """
    print(Available_Services.get_json_list())
    print(Allowed_File_Formats.get_json_list())


if __name__ == "__main__":
    import doctest

    doctest.testmod()
