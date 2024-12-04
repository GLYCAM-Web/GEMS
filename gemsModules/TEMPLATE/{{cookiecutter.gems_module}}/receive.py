#!/usr/bin/env python3
from gemsModules.{{cookiecutter.gems_module}}.json_string_manager import {{cookiecutter.gems_module}}_Json_String_Manager
from gemsModules.{{cookiecutter.gems_module}}.main_settings import WhoIAm
from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


def receive(incomingString: str) -> str:
    log.info("{{cookiecutter.gems_module}} was called as an entity.  Processing.")
    {{cookiecutter.gems_module}}_manager = {{cookiecutter.gems_module}}_Json_String_Manager()
    {{cookiecutter.gems_module}}_manager_error_response = {{cookiecutter.gems_module}}_manager.process(incoming_string = incomingString)
    if {{cookiecutter.gems_module}}_manager_error_response is not None:
        log.debug("The incoming string is not valid")
        return {{cookiecutter.gems_module}}_manager_error_response
    log.debug("The incoming string is valid")
    return {{cookiecutter.gems_module}}_manager.transaction.get_outgoing_string()
