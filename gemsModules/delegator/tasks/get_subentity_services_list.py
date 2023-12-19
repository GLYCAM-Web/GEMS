import importlib
from gemsModules.delegator.redirector_settings import Known_Entity_Modules

from typing import List, Dict


def execute(entity: str) -> List:
    """Return a list of available services"""
    # Known_Entity_Modules[entity] == the module, but it's .tasks isn't initialized yet so we must import it using the laoded module
    # Known_Entity_Modules[entity].tasks.get_services_list.execute() == the function we want to call
    service_list = importlib.import_module(
        Known_Entity_Modules[entity]
    ).tasks.get_services_list.execute()
    return service_list


if __name__ == "__main__":
    import doctest

    doctest.testmod()
