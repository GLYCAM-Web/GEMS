from gemsModules.delegator.services.settings.known_available import Available_Services
from typing import List, Dict


def execute(entity: str) -> List:
    """Return a list of available services

    >>> print(execute())
    ['Error', 'Marco', 'Status', 'ListServices', 'KnownEntities']

    """

    return Available_Services.get_json_list()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
