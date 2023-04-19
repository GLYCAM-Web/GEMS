#!/usr/bin/env python3
from pydantic import BaseModel, Field

from gemsModules.common.main_api_services import Service_Request, Service_Response

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)

# I'm writing this non-abstractly in delegator first.  After I get it working, I'll
#    move it to common and make it abstract.

class marco_Inputs(BaseModel) :
    entity : str  = Field(
        'Delegator',
        description="The entity to which the Marco request is sent.")
    who_I_am : str = Field(
        'Delegator',
        description="The name of the entity receiving the Marco request.  Written by GEMS.")
    
class marco_Outputs(BaseModel) :
    message : str  = Field(
        None,
        description="The response to the Marco request.")

class marco_Request(Service_Request) :
    typename : str  = Field(
        "Marco",   
        alias='type'
    )
    inputs : marco_Inputs = marco_Inputs()

class marco_Response(Service_Response) :
    typename : str  = Field(
        "Marco",   
        alias='type'
    )
    outputs : marco_Outputs = marco_Outputs()
