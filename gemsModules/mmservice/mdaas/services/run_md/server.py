#!/usr/bin/env python3
from gemsModules.mmservice.mdaas.services.run_md.run_md_api import (
    run_md_Request,
    run_md_Response,
)
from gemsModules.common.tasks import cake

from gemsModules.mmservice.mdaas.services.run_md.logic import execute

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class cakeInputs:
    cake: bool = False
    color: str = None


def Serve(service_request: run_md_Request) -> run_md_Response:
    log.debug("SERVE: run_md")

    response = run_md_Response()
    response.outputs = execute(service_request.inputs)

    # run_md request doesn't normally contain the entity/who_am_i info.
    # The who_I_am must be set in the options.
    # if (
    #     service_request.entity == service_request.who_I_am
    # ):  # trivial here, but could be more complex (search a dictionary, etc.).
    #     response.outputs.message = "Polo"
    # else:
    #     response.outputs.message = (
    #         "Marco request sent to wrong entity. See who_I_am in info."
    #     )

    if service_request.options is not None:
        cake_inputs = cakeInputs()
        docake = False
        if "cake" in service_request.options.keys():
            docake = True
            cake_inputs.cake = service_request.options["cake"]
        if "color" in service_request.options.keys():
            docake = True
            cake_inputs.color = service_request.options["color"]
        if docake == True:
            response.outputs.info = cake.execute(cake_inputs)

    response.outputs.projectDir = service_request.inputs.projectDir
    return response
