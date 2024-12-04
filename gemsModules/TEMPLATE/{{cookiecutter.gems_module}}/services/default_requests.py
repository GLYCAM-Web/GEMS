#!/usr/bin/env python3
from typing import List
import uuid

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.default_requests import Default_Service_Request_Manager

from gemsModules.{{cookiecutter.gems_module}}.main_api import {{cookiecutter.gems_module}}_Service_Request
                   
from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class {{cookiecutter.gems_module}}_Default_Service_Request_Manager(Default_Service_Request_Manager):

    def get_default_services_aaops(self) -> List[AAOP]:
        this_service = {{cookiecutter.gems_module}}_Service_Request()
        this_aaop = AAOP(
            AAO_Type="{{cookiecutter.service_name}}",
            The_AAO=this_service,
            ID_String=uuid.uuid4(),
            Dictionary_Name="default_{{cookiecutter.service_name}}",
            )
        return [this_aaop]
