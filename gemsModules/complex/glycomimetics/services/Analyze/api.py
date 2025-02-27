#!/usr/bin/env python3
from pydantic import BaseModel, Field, validator
from typing import List, Union

from gemsModules.common.main_api_resources import Resource, Resources

from gemsModules.complex.glycomimetics.main_api import (
    Glycomimetics_Service_Request,
    Glycomimetics_Service_Response,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Analyze_input_Resource(Resource):
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


class Analyze_output_Resource(Resource):
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


class Analyze_Resources(Resources):
    __root__: List[Union[Analyze_input_Resource, Analyze_output_Resource]] = None


class Analyze_Inputs(BaseModel):
    pUUID: str = Field(
        None,
        title="Project UUID",
        description="UUID of Project",
    )

    # The problem here is that we would need to change request to not initialize an empty inputs.
    # @validator("pUUID", always=True)
    def check_uuid(cls, v):
        if not v:
            raise ValueError("Project UUID must be provided")
        return v

    resources: Analyze_Resources = Analyze_Resources()


class Analyze_Outputs(BaseModel):
    outputDirPath: str = Field(
        None,
        title="Output Directory Path",
        description="Path to output directory",
    )
    resources: Analyze_Resources = Analyze_Resources()


class Analyze_Request(Glycomimetics_Service_Request):
    typename: str = Field("Analyze", alias="type")
    # the following must be redefined in a child class
    inputs: Analyze_Inputs = Analyze_Inputs()


class Analyze_Response(Glycomimetics_Service_Response):
    typename: str = Field("Analyze", alias="type")
    outputs: Analyze_Outputs = Analyze_Outputs()
