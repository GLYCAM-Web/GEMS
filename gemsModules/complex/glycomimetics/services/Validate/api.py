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


class Validate_input_Resource(Resource):
    """Need to write validators."""

    ## Works now:
    ##
    ## locationType = filepath
    ##
    ## resourceFormat = amber_parm7 | amber_rst7 | md_path | max_hours
    ##
    ## payload = string containing a /path/to/file  |  integer (number of hours)
    ##
    ## options = none currently read
    ##
    pass


class Validate_output_Resource(Resource):
    """Need to write validators."""

    ## Works now:
    ##
    ## locationType = filepath
    ##
    ## resourceFormat = amber_parm7 | amber_rst7 | amber_nc | amber_mdcrd | amber_mdout | zipfile
    ##
    ## payload = string containing a /path/to/file
    ##
    ## notices = these will surely happen
    ##
    pass


class Validate_Resources(Resources):
    __root__: List[
        Union[PDB_File_Resource, Validate_input_Resource, Validate_output_Resource]
    ] = None


class Validate_Inputs(BaseModel):
    pUUID: str = Field(
        None,
        title="Project UUID",
        description="UUID of Project",
    )

    # TODO: should be receptor_path which is a local fs path
    receptor: Optional[str] = Field(
        None,
        title="Receptor",
        description="Receptor PDB file",
    )

    # TODO: see Build.api too, we need to use service specific resources for better constraints.
    # resources: Validate_Resources = Validate_Resources()
    resources: Resources = Resources()


class Validate_Outputs(BaseModel):
    isValid: bool = Field(
        None,
        title="Is Valid",
        description="Is the input valid",
    )


class Validate_Request(Glycomimetics_Service_Request):
    typename: str = Field("Validate", alias="type")
    # the following must be redefined in a child class
    inputs: Validate_Inputs = Validate_Inputs()


class Validate_Response(Glycomimetics_Service_Response):
    typename: str = Field("Validate", alias="type")
    outputs: Validate_Outputs = Validate_Outputs()
