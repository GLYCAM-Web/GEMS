#!/usr/bin/env python3
from pydantic import ValidationError
from gemsModules.common.json_string_manager import Json_String_Manager
from gemsModules.{{cookiecutter.gems_module}}.main_settings import WhoIAm
from gemsModules.{{cookiecutter.gems_module}}.main_api import {{cookiecutter.gems_module}}_Transaction
from gemsModules.{{cookiecutter.gems_module}}.transaction_manager import {{cookiecutter.gems_module}}_Transaction_Manager

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class {{cookiecutter.gems_module}}_Json_String_Manager(Json_String_Manager):

    def get_local_components(self):
        self.transaction = {{cookiecutter.gems_module}}_Transaction()
        self.entityType = WhoIAm
        self.transaction_manager_type = {{cookiecutter.gems_module}}_Transaction_Manager
