#!/usr/bin/env python3

from gemsModules.common.transaction_manager import Transaction_Manager
from gemsModules.common.services.aaop_tree_pair_manager import AAOP_Tree_Pair_Generator
from gemsModules.{{cookiecutter.gems_module}}.project_manager import {{cookiecutter.service_name}}_Project_Manager
from gemsModules.{{cookiecutter.gems_module}}.services.request_manager import {{cookiecutter.service_name}}_Request_Manager
from gemsModules.{{cookiecutter.gems_module}}.services.response_manager import {{cookiecutter.service_name}}_Response_Manager
from gemsModules.{{cookiecutter.gems_module}}.services.servicer import {{cookiecutter.service_name}}_Servicer

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)

class {{cookiecutter.service_name}}_Transaction_Manager(Transaction_Manager):

    def set_local_modules(self):
        self.request_manager_type =  {{cookiecutter.service_name}}_Request_Manager
        self.aaop_tree_pair_manager_type = AAOP_Tree_Pair_Generator
        self.this_servicer_type = {{cookiecutter.service_name}}_Servicer
        self.response_manager_type = {{cookiecutter.service_name}}_Response_Manager
        self.project_manager_type = {{cookiecutter.service_name}}_Project_Manager
   


