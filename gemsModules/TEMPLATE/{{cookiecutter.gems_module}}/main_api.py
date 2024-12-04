#!/usr/bin/env python3
from pydantic import  Field
from typing import Literal, Dict
from gemsModules.common import main_api
from gemsModules.common import main_api_entity
from gemsModules.common import main_api_services

from gemsModules.{{cookiecutter.gems_module}}.main_settings import WhoIAm
from gemsModules.{{cookiecutter.gems_module}}.main_api_project import {{cookiecutter.gems_module}}_Project
from gemsModules.{{cookiecutter.gems_module}}.services.settings.known_available import Available_Services
from gemsModules.{{cookiecutter.gems_module}}.services.{{cookiecutter.service_name}}.api import {{cookiecutter.service_name}}Service_Request, {{cookiecutter.service_name}}Service_Response
from gemsModules.{{cookiecutter.gems_module}}.main_api_common import {{cookiecutter.gems_module}}_Service_Request, {{cookiecutter.gems_module}}_Service_Response

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class {{cookiecutter.gems_module}}_Service_Requests(main_api_services.Service_Requests):
    __root__ : dict[str, {{cookiecutter.service_name}}Service_Request, {{cookiecutter.gems_module}}_Service_Request] = None


class {{cookiecutter.gems_module}}_Service_Responses(main_api_services.Service_Responses):
    __root__ : dict[str, {{cookiecutter.service_name}}Service_Response, {{cookiecutter.gems_module}}_Service_Response] = None


class {{cookiecutter.gems_module}}_Entity(main_api_entity.Entity) :

    entityType : Literal['{{cookiecutter.gems_module}}'] = Field(  # This is the only required field in all of the API
            ...,
            title='Type',
            alias='type'
            )
    services : {{cookiecutter.gems_module}}_Service_Requests = {{cookiecutter.gems_module}}_Service_Requests()  
    responses : {{cookiecutter.gems_module}}_Service_Responses = {{cookiecutter.gems_module}}_Service_Responses()


class {{cookiecutter.gems_module}}_API(main_api.Common_API):
    entity : {{cookiecutter.gems_module}}_Entity
    project : {{cookiecutter.gems_module}}_Project = {{cookiecutter.gems_module}}_Project()


class {{cookiecutter.gems_module}}_Transaction(main_api.Transaction):
    
    def get_API_type(self):  # This allows dependency injection in the children
        return {{cookiecutter.gems_module}}_API


