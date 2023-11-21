from gemsModules.delegator.redirector_settings import (
    Known_Entities,
    Known_Entity_Reception_Modules,
)
from typing import List


def execute() -> List:
    """Return a list of entities known to the Delegator
    >>> print(execute())
    ['Delegator', 'DeprecatedDelegator', 'MDaaS', 'Status', 'BatchCompute', 'Conjugate', 'Common', 'MmService', 'Query', 'Sequence', 'DrawGlycan', 'StructureFile']
    """

    return list(Known_Entity_Reception_Modules.keys())


if __name__ == "__main__":
    import doctest

    doctest.testmod()
