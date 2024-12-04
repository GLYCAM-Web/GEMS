#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.request_data_filler import Request_Data_Filler

from gemsModules.{{cookiecutter.gems_module}}.main_api import {{cookiecutter.gems_module}}_Entity
from gemsModules.{{cookiecutter.gems_module}}.main_api_project import {{cookiecutter.gems_module}}_Project

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


class {{cookiecutter.gems_module}}_Request_Data_Filler(Request_Data_Filler):

        # self.aaop_list = aaop_list
        # self.entity = entity
        # self.project = project

    # No data to fill here.
    def process(self) -> List[AAOP]:
        for aaop in self.aaop_list:
            if aaop.Dictionary_Name=='{{cookiecutter.service_name}}':
                from gemsModules.{{cookiecutter.gems_module}}.services.{{cookiecutter.service_name}} import api
                this_Project : {{cookiecutter.gems_module}}_Project = self.project
                aaop.The_AAO.inputs.pUUID=this_Project.pUUID

        return self.aaop_list
