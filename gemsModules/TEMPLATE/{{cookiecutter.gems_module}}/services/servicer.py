#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Callable

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.action_associated_objects import AAOP_Tree_Pair

from gemsModules.common.services.servicer import Servicer

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


class {{cookiecutter.gems_module}}_Servicer(Servicer):

    def get_module_for_this_request(self, this_request_aaop: AAOP) -> Callable:
        from gemsModules.{{cookiecutter.gems_module}}.services.settings.service_modules import service_modules
        return service_modules[this_request_aaop.AAO_Type]
       
