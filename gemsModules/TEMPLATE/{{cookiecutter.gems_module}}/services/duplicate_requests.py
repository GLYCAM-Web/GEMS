#!/usr/bin/env python3
from typing import List, Callable

from gemsModules.common.services.duplicate_requests import Duplicate_Requests_Manager

from gemsModules.{{cookiecutter.gems_module}}.tasks import get_services_list
from gemsModules.{{cookiecutter.gems_module}}.services.settings.duplicates_modules import duplicates_modules 

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class {{cookiecutter.gems_module}}_Duplicate_Requests_Manager(Duplicate_Requests_Manager):

    def get_available_services(self) -> List[str]:
        return get_services_list.execute()

    def get_duplicates_manager(self, service : str) -> Callable:
        return duplicates_modules[service]
        
