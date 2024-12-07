from gemsModules.common.code_utils import GemsStrEnum

from gemsModules.common.services.settings.known_available import (
    Module_Available_Services as Common_Available_Services,
)
from gemsModules.common.services.settings.known_available import (
    Multiples_Action as Common_Multiples_Action,
)
from gemsModules.common.services.settings.known_available import (
    Request_Conflict_Action as Common_Request_Conflict_Action,
)


from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Module_Available_Services(GemsStrEnum):
    known_entities = "KnownEntities"
    listEntities = "listEntities"  # old json contract compatibility
    ListEntities = (
        "ListEntities"  # json contract compatibility (what it should have been)
    )


Available_Services = GemsStrEnum(
    "Available_Services",
    [(avail.name, avail.value) for avail in Common_Available_Services]
    + [(avail.name, avail.value) for avail in Module_Available_Services],
)

Module_Multiples_Action = {
    "KnownEntities": "Merge",
}

Multiples_Action = dict(Common_Multiples_Action)
Multiples_Action.update(Module_Multiples_Action)

Module_Request_Conflict_Action = {
    "KnownEntities": "LastIn",
}
Request_Conflict_Action = dict(Common_Request_Conflict_Action)
Request_Conflict_Action.update(Module_Request_Conflict_Action)


def testme():
    """Ensure that the settings info is complete.
    >>> testme()
    ['Error', 'Marco', 'Status', 'ListServices', 'KnownEntities']
    {'Error': 'All', 'Marco': 'Merge', 'Status': 'Merge', 'ListServices': 'Merge', 'KnownEntities': 'Merge'}
    {'Error': 'FirstIn', 'Marco': 'Fail', 'Status': 'LastIn', 'ListServices': 'LastIn', 'KnownEntities': 'LastIn'}

    """
    print(Available_Services.get_json_list())
    print(Multiples_Action)
    print(Request_Conflict_Action)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
