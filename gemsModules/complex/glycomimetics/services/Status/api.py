#!/usr/bin/env python3
from pydantic import BaseModel, Field, ValidationError, validator
from typing import List, Optional, Union

from gemsModules.common.main_api_resources import Resource, Resources

from gemsModules.complex.glycomimetics.main_api import (
    Glycomimetics_Service_Request,
    Glycomimetics_Service_Response,
)
from gemsModules.complex.glycomimetics.services.common_api import PDB_File_Resource

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
        Union[PDB_File_Resource, Status_input_Resource, Status_output_Resource]
    ] = None


class Status_Inputs(BaseModel):
    pUUID: str = Field(
        None,
        title="Project UUID",
        description="UUID of Project",
    )

    receptor: Optional[str] = Field(
        None,
        title="Receptor",
        description="Receptor PDB file",
    )

    # TODO: see Build.api too and fix this
    # resources: Status_Resources = Status_Resources()
    resources: Resources = Resources()


class Status_Outputs(BaseModel):
    isValid: bool = Field(
        None,
        title="Is Valid",
        description="Is the input valid",
    )


class Status_Request(Glycomimetics_Service_Request):
    typename: str = Field("Status", alias="type")
    # the following must be redefined in a child class
    inputs: Status_Inputs = Status_Inputs()


class Status_Response(Glycomimetics_Service_Response):
    typename: str = Field("Status", alias="type")
    outputs: Status_Outputs = Status_Outputs()
