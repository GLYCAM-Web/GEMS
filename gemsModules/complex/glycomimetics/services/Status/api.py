#!/usr/bin/env python3
from enum import auto
from pydantic import BaseModel, Field, ValidationError, validator
from typing import List, Optional, Union

from gemsModules.common.main_api_resources import Resource, Resources

# from gemsModules.complex.glycomimetics.main_api import (
#     Glycomimetics_Service_Request,
#     Glycomimetics_Service_Response,
# )
from gemsModules.common.main_api_services import (
    Service_Request,
    Service_Response,
)
    
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Status_input_Resource(Resource):
    """Need to write validators."""
    pass


class Status_output_Resource(Resource):
    """Need to write validators."""
    pass


class Status_Resources(Resources):
    __root__: List[
        Union[Status_input_Resource, Status_output_Resource]
    ] = None


class Status_Inputs(BaseModel):
    pUUID: str = Field(
        None,
        title="Project UUID",
        description="UUID of Project",
    )

    # TODO: see Build.api too and fix this
    # resources: Status_Resources = Status_Resources()
    resources: Resources = Resources()


class StatusEnum(str):
    Success = auto()
    Failure = auto()
    Pending = auto()
    Running = auto()
    NotFound = auto()

class Status_Outputs(BaseModel):
    status: StatusEnum = Field(
        None,
        title="Status",
        description="Status of the project being checked",
    )
    details: Optional[str] = Field(
        None,
        title="Details",
        description="Details about the project status",
    )
        

class Status_Request(Service_Request):
    typename: str = Field("Status", alias="type")
    # the following must be redefined in a child class
    inputs: Status_Inputs = Status_Inputs()


class Status_Response(Service_Response):
    typename: str = Field("Status", alias="type")
    outputs: Status_Outputs = Status_Outputs()
