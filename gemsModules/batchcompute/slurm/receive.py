#!/usr/bin/env python3
import sys, os
import traceback

import grpc

import gemsModules.deprecated
import gemsModules.deprecated.batchcompute.settings as batchcomputeSettings

from gemsModules.deprecated import common
from gemsModules.deprecated.common.services import *
from gemsModules.deprecated.common.transaction import *  # might need whole file...
from gemsModules.deprecated.batchcompute.slurm.dataio import *
from gemsModules.deprecated.batchcompute.slurm.receive import manageIncomingString

from gemsModules.mmservice.mdaas.tasks import create_slurm_submission

from gemsModules.networkconnections.grpc import (
    slurm_grpc_submit,
    is_GEMS_instance_for_SLURM_submission,
)
from gemsModules.systemoperations.instance_ops import InstanceConfig
from gemsModules.systemoperations.environment_ops import is_GEMS_test_workflow
from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


# TODO: TO a task?
def run_slurm_submission_script(thisSlurmJobInfo):
    log.debug("run_slurm_submission_script() was called.\n")
    import os, sys, subprocess, signal
    from subprocess import Popen

    if "sbatchArgument" not in thisSlurmJobInfo.incoming_dict.keys():
        return "SLURM submit cannot find sbatch submission arguments."

    if thisSlurmJobInfo.incoming_dict["workingDirectory"] is not None:
        try:
            os.chdir(thisSlurmJobInfo.incoming_dict["workingDirectory"])
        except Exception as error:
            log.error("Was unable to change to the working directory.")
            log.error("Error type: " + str(type(error)))
            log.error(traceback.format_exc())
            return "Was unable to change to the working directory."
    log.debug("The current directory is:  " + os.getcwd())
    try:
        log.debug(
            "In func run_slurm_submission_script, incoming dict sbatchArg is: "
            + thisSlurmJobInfo.incoming_dict["sbatchArgument"]
            + "\n"
        )
        p = subprocess.Popen(
            ["sbatch", thisSlurmJobInfo.incoming_dict["slurm_runscript_name"]],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        (outputhere, errorshere) = p.communicate()
        if p.returncode != 0:
            return "SLURM submit got non-zero exit upon attempt to submit."
        else:
            log.debug("outputhere in raw form: " + str(outputhere))
            theOutput = outputhere.decode("utf-8")
            log.debug("outputhere stripped: " + theOutput)
            return theOutput
    except Exception as error:
        log.error("Was unable to submit the job.")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc())
        return "Was unable to submit the job."


def receive(jsonObjectString):
    """
    TODO write me a docstring
    """
    import os, sys, socket

    log.info("batchcompute.slurm.receive() was called.\n")
    log.debug(
        "incoming jsonObjectString: \n" + str(jsonObjectString)
    )  # Actually a dict? SlurmJobInfo?

    # Make a new SlurmJobInfo object for holding I/O information.
    # TODO: newstyle gemsModule
    thisSlurmJobInfo = SlurmJobInfo(jsonObjectString)
    thisSlurmJobInfo.parseIncomingString()

    thisSlurmJobInfo.incoming_dict["slurm_runscript_name"] = "slurm_submit.sh"
    slurm_runscript_path = (
        thisSlurmJobInfo.incoming_dict["workingDirectory"]
        + "/"
        + thisSlurmJobInfo.incoming_dict["slurm_runscript_name"]
    )
    log.debug("Slurm runscript path: " + slurm_runscript_path + "\n")
    if os.path.exists(slurm_runscript_path):
        log.debug("Found existing Slurm run script.  Refusing to clobber.")
    else:
        log.debug("Writing a new Slurm run script.")
        create_slurm_submission.execute(slurm_runscript_path, thisSlurmJobInfo)

    # If grpc-delegator, we want to reroute to the correct host with gRPC.
    # See instance_config.json for info on available hosts and contexts.

    if is_GEMS_instance_for_SLURM_submission(requested_ctx="MDaaS-RunMD"):
        response = run_slurm_submission_script(thisSlurmJobInfo)
        if response is None:
            log.error("Got none response")
            # TODO: return a proper error response.
        else:
            thisSlurmJobInfo.copyJobinfoInToOut()
            thisSlurmJobInfo.addSbatchResponseToJobinfoOut(response)
            log.debug("The outgoing dictionary is: \n")
            log.debug(str(thisSlurmJobInfo.outgoing_dict))
            log.debug("\n")

            return thisSlurmJobInfo.outgoing_dict
    else:
        addresses = InstanceConfig().get_possible_hosts_for_context(
            "MDaaS-RunMD", with_slurmport=True
        )
        # just using first host for now, we could try slurm_grpc_submit, and if it fails, go down the list
        host, port = addresses[0].split(":")

        failed = False
        tried = []
        while len(addresses):
            h, p = addresses.pop().split(":")
            try:
                response = slurm_grpc_submit(jsonObjectString, host=h, port=p)
                failed = False
                break
            except grpc.RpcError:
                failed = True
                log.warning(
                    "Failed to submit to %s:%s. Trying next host in list.",
                    h,
                    p,
                    exc_info=True,
                )
            finally:
                tried.append(h)

        if failed:
            # maybe should be error?
            log.warning(
                "All attempts to make a SLURM submission over gRPC failed. servers tried: %s",
                tried,
            )

        if response is None:
            log.error("Got none response")

        return response


# def main():
#     import importlib.util, os, sys

#     # from importlib import util
#     if importlib.util.find_spec("deprecated") is None:
#         this_dir, this_filename = os.path.split(__file__)
#         sys.path.append(this_dir + "/../../")
#         if importlib.util.find_spec("common") is None:
#             print("I cannot find the Common Servicer.  No clue what to do. Exiting")
#             sys.exit(1)
#         else:
#             from common import utils
#     else:
#         from gemsModules.deprecated.common import utils
#     jsonObjectString = utils.JSON_From_Command_Line(sys.argv)
#     try:
#         thisSlurmJobInfo = manageIncomingString(jsonObjectString)
#     except Exception as error:
#         print("\nThe Slurm Job info string manager captured an error.")
#         print("Error type: " + str(type(error)))
#         print(traceback.format_exc())
#         ##TODO: see about exploring this error and returning more info. Temp solution for now.
#     try:
#         submit(thisSlurmJobInfo)
#     except Exception as error:
#         print("\nThe Slurm Job sumbit module captured an error.")
#         print("Error type: " + str(type(error)))
#         print(traceback.format_exc())

#     print("\ndelegator is returning this: \n" + responseObjectString)
#

# if __name__ == "__main__":
#     main()
