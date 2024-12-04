#!/usr/bin/env python3
from pydantic import  Field
from gemsModules.common import main_api_services

from gemsModules.{{cookiecutter.gems_module}}.main_api_project import {{cookiecutter.gems_module}}_Project
from gemsModules.{{cookiecutter.gems_module}}.services.settings.known_available import Available_Services

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class {{cookiecutter.gems_module}}_Service_Request(main_api_services.Service_Request):
    typename : Available_Services = Field(
        '{{cookiecutter.service_name}}',
        alias='type',
        title='Services Offered by {{cookiecutter.gems_module}}',
        description='The service requested of the {{cookiecutter.gems_module}}'
    )


class {{cookiecutter.gems_module}}_Service_Response(main_api_services.Service_Response):
    typename : Available_Services = Field(
        None,
        alias='type',
        title='Services Offered by {{cookiecutter.gems_module}}',
        description='The service requested of {{cookiecutter.gems_module}}'
    )