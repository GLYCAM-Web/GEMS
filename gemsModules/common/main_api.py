#!/usr/bin/env python3
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Dict

from gemsModules.project.main_api import Project
from gemsModules.common.main_api_entity import Entity
from gemsModules.common.main_api_notices import Notices
from gemsModules.common import settings as settings_main

import traceback

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Common_API(BaseModel):
    timestamp: str = None
    entity: Entity  # The only required part of the JSON is the entity.
    project: Project = None
    notices: Notices = Notices()
    prettyPrint: bool = None  ## this is a change from the original
    mdMinimize: bool = None  ## this is a change from the original
    options: Dict[str, str] = Field(
        None, description="Key-value pairs that apply to the entire transaction."
    )

    def copy_procedural_options_to_entity(self):
        if self.prettyPrint is not None:
            self.entity.procedural_options.pretty_print = self.prettyPrint
        if self.mdMinimize is not None:
            self.entity.procedural_options.md_minimize = self.mdMinimize


class Transaction(ABC):
    @abstractmethod
    def get_API_type(self):  # This allows dependency injection in the children
        return Common_API
        ## If you want to use the schema from this abstract parent without having
        ##    to hand-code 'Common_API", you can do this:
        ##
        ##    return super().get_API_type()
        ##
        ## To check that it does what you think, you can do something like this:
        ##
        ##    __super__ = super().get_API_type()
        ##    print("The api type is " + str(__super__))

    def __init__(self):
        self.incoming_string: str = None
        self.inputs: self.get_API_type() = None
        self.outputs: self.get_API_type() = None
        #        self.inputs : Common_API = None
        #        self.outputs : Common_API = None
        self.outgoing_string: str = None

    def process_incoming_string(
        self,
        in_string: str,  # The JSON input string
        no_check_fields=False,  # Do not perform a check of fields vs schema using Pydantic
        initialize_out=True,  # Initialize an outgoing transaction from the incoming one
    ):
        try:
            log.debug(f"incoming string is: \n{in_string}\n")
            self.incoming_string = in_string
            if self.incoming_string is None or self.incoming_string == "":
                log.error("incoming string was empty")
                self.generate_error_response(Brief="InvalidInput")
                return 1
            self.populate_inputs(in_string=in_string, no_check_fields=no_check_fields)
            if initialize_out:
                self.initialize_outputs_from_inputs()
            return None
        except Exception as error:
            # TODO: Clean this up, looks doubled up.
            errMsg = "problem processing this string: " + str(in_string)
            log.error(errMsg)
            log.error(error)
            log.error(traceback.format_exc())
            log.debug("problem processing this string: " + str(in_string))
            log.debug("the error message is: ")
            log.debug(error)
            self.generate_error_response(
                Brief="JsonParseEror", AdditionalInfo={"error": str(error)}
            )
            #            return 1
            raise

    def populate_inputs(self, in_string: str, no_check_fields=False):
        self.inputs = self.get_API_type().parse_raw(in_string)
        log.debug("The inputs are: ")
        log.debug(self.inputs.json(indent=2))

    def initialize_outputs_from_inputs(self):
        log.info("initialize_outputs_from_inputs was called")
        self.outputs = self.get_API_type()
        self.outputs = self.inputs.copy(deep=True)

    # the use of EntityType here will break elsewhere, I think
    def generate_error_response(
        self, Brief="UnknownError", EntityType=settings_main.WhoIAm, AdditionalInfo=None
    ):
        self.outputs = self.get_API_type().construct(
            entity=Entity.construct(entityType=settings_main.WhoIAm)
        )
        if self.outputs.notices is None:
            self.outputs.notices = Notices()
        self.outputs.notices.addDefaultNotice(
            Brief=Brief, Messenger=settings_main.WhoIAm, AdditionalInfo=AdditionalInfo
        )
        self.build_outgoing_string()

    def build_outgoing_string(
        self, prettyPrint=False, indent=2, prune_empty_values=True
    ):
        if (
            self.outputs.prettyPrint is True
        ):  # In case outputs.prettyPrint is None or something else that isn't useful
            prettyPrint = True
        if prettyPrint:
            self.outgoing_string = self.outputs.json(
                indent=2, exclude_none=prune_empty_values, by_alias=True
            )
        else:
            self.outgoing_string = self.outputs.json(
                exclude_none=prune_empty_values, by_alias=True
            )

    def get_outgoing_string(self, prettyPrint=False, indent=2, prune_empty_values=True):
        if self.outgoing_string is None or self.outgoing_string == "":
            try:
                self.build_outgoing_string(prettyPrint, indent, prune_empty_values)
            except Exception as error:
                log.debug("There was an error building the outgoing string")
                log.debug(error)
                self.generate_error_response()
        return self.outgoing_string

    def get_input_services(self):
        return self.inputs.entity.services

    def generate_schema(self):
        return self.get_API_type().schema_json(indent=2)


def generateSchema():
    print(Common_API.schema_json(indent=2))


class common_Transaction(Transaction):
    def get_API_type(self):
        return Common_API
