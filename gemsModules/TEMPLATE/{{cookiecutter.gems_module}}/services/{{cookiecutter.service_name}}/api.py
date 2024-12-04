#!/usr/bin/env python3
from pydantic import BaseModel, Field
from typing   import List, Union, Optional

from gemsModules.common.main_api_resources import Resource, Resources
from gemsModules.{{cookiecutter.gems_module}}.main_api_common import {{cookiecutter.gems_module}}_Service_Request, {{cookiecutter.gems_module}}_Service_Response

from gemsModules.logging.logger import Set_Up_Logging 


log = Set_Up_Logging(__name__)


class {{cookiecutter.service_name}}Service_input_Resource(Resource):
    """ Need to write validators. """
    pass

class {{cookiecutter.service_name}}Service_output_Resource(Resource):
    """ Need to write validators. """
    pass

class {{cookiecutter.service_name}}Service_Resources(Resources):
    __root__ : List[Union[{{cookiecutter.service_name}}Service_input_Resource, {{cookiecutter.service_name}}Service_output_Resource]] = None


class {{cookiecutter.service_name}}Service_Inputs(BaseModel) :
    pUUID : str = Field(
        None,
        title='Project UUID',
        description='UUID of Project',
    )
    resources : Optional[{{cookiecutter.service_name}}Service_Resources] = Field(
        title='Resources',
        description='Resources for {{cookiecutter.service_name}}',
        default_factory={{cookiecutter.service_name}}Service_Resources
    )
    
    
class {{cookiecutter.service_name}}Service_Outputs(BaseModel) :
    message : str = Field(
        "",
        title='{{cookiecutter.service_name}} response',
        description='A nice message to return.',
    )
    resources : Optional[{{cookiecutter.service_name}}Service_Resources] = Field(
        title='Resources',
        description='Resources for {{cookiecutter.service_name}}',
        default_factory={{cookiecutter.service_name}}Service_Resources
    )


class {{cookiecutter.service_name}}Service_Request({{cookiecutter.gems_module}}_Service_Request) :
    typename : str  = Field(
        "{{cookiecutter.service_name}}",   
        alias='type'
    )
    # the following must be redefined in a child class
    inputs : {{cookiecutter.service_name}}Service_Inputs = {{cookiecutter.service_name}}Service_Inputs()

class {{cookiecutter.service_name}}Service_Response({{cookiecutter.gems_module}}_Service_Response) :
    typename : str  = Field(
        "{{cookiecutter.service_name}}",   
        alias='type'
    )
    outputs : {{cookiecutter.service_name}}Service_Outputs = {{cookiecutter.service_name}}Service_Outputs()
