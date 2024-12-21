#!/usr/bin/env python3
from gemsModules.complex.glycomimetics.json_string_manager import (
    Glycomimetics_Json_String_Manager,
)
from gemsModules.complex.glycomimetics.main_settings import WhoIAm
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def receive(incomingString: str) -> str:
    log.info("Glycomimetics was called as an entity.  Processing.")
    Glycomimetics_manager = Glycomimetics_Json_String_Manager()
    Glycomimetics_manager_error_response = Glycomimetics_manager.process(
        incoming_string=incomingString
    )

    if Glycomimetics_manager_error_response is not None:
        log.debug("The incoming string is not valid")
        return Glycomimetics_manager_error_response

    log.debug("The incoming string is valid")
    
    # Write the response to a a file in the project directory
    output_path = Glycomimetics_manager.transaction.outputs.project.project_dir
    response_json_path = output_path + "/response.json"
    with open(response_json_path, "w") as f:
        f.write(Glycomimetics_manager.transaction.get_outgoing_string(prettyPrint=True))
        f.write("\n")
    
    # Return the response in a condensed format for the API
    return Glycomimetics_manager.transaction.get_outgoing_string()
