#!/usr/bin/env python3
from gemsModules.delegator.json_string_manager import Redirector_Json_String_Manager
from gemsModules.delegator.json_string_manager import Delegator_Json_String_Manager
from gemsModules.delegator.main_settings import WhoIAm
from gemsModules.logging.logger import Set_Up_Logging

from gemsModules.delegator import redirector_settings

log = Set_Up_Logging(__name__)


def process(incomingString: str) -> str:
    log.info("Delegator was called as an entity.  Processing.")
    delegator_string_manager = Delegator_Json_String_Manager()
    delegator_string_manager_error_response = delegator_string_manager.process(
        incoming_string=incomingString
    )
    if delegator_string_manager_error_response is not None:
        log.debug("The incoming string is not valid")
        return delegator_string_manager_error_response
    else:
        log.debug("The incoming string is valid")
        return delegator_string_manager.transaction.get_outgoing_string()


def receive(incomingString: str) -> str:
    log.info("Delegator's receive was called")

    string_manager = Redirector_Json_String_Manager()

    string_manager_error_response_string = string_manager.process(
        incoming_string=incomingString
    )

    if string_manager_error_response_string is not None:
        log.debug("The incoming string is not valid")
        log.debug("The incoming string (incomingString) is: ")
        log.debug(incomingString)
        log.debug("The error response string (receiver_error_response_string) is: ")
        log.debug(string_manager_error_response_string)
        return string_manager_error_response_string

    log.debug("The incoming string is valid")
    requested_entity = string_manager.get_incoming_entity_type()

    if requested_entity == WhoIAm:
        log.debug("Delegating incoming string to self")
        return process(incomingString)
    else:
        log.debug("Delegating incoming string to entity: " + requested_entity)

        entity_module = redirector_settings.Known_Entity_Reception_Modules[
            requested_entity
        ]
        return entity_module.receive(incomingString)
