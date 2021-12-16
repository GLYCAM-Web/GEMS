#!/usr/bin/env python3
import gemsModules
from gemsModules.batchcompute.receive import *
from gemsModules import common
from gemsModules.common.services import *
from gemsModules.common.transaction import * # might need whole file...
from gemsModules.common.loggingConfig import *
from gemsModules.project.projectUtil import *
from gemsModules.structureFile.amber.preprocess import preprocessPdbForAmber
import gemsModules.conjugate.settings as conjugateSettings
import gemsModules.conjugate.io as conjugateio
import subprocess
import urllib.request

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

###
### For conjugate, the default is Marco-Polo, maybe with help text.
###
def doDefaultService(jsonObjectString):
    log.info("doDefaultService() was called.\n")
    thisTransaction=conjugateio.Transaction(jsonObjectString)
    thisTransaction.outputs.entity.entityType=settings.WhoIAm
    thisTransaction.outputs.entity.responses=[]
    thisTransaction.outputs.entity.responses.append({'payload':marco('Conjugate')})
    return thisTransaction


def receive(jsonObjectString, entityType=None):
    log.info("receive() in conjugate was called.\n")
    if entityType is None:
        entityType = getEntityTypeFromJson(jsonObjectString)
        if entityType is None: 
            return buildInvalidInputErrorResponseJsonString(
                    thisMessagingEntity=settings.WhoIAm,
                    message="entity type not found in json input string")

    if entityType == 'Glycoprotein':
        returnedTransaction = glycoprotein.receive.receive(
                    jsonObjectString,
                    entityType=entityType)
        return returnedTransaction


    ##Look in transaction for the requested service. If none, do default service.
    if 'services' not in jsonObjectString:
        log.debug("could not find the services in the input - calling default")
        doDefaultService(jsonObjectString)

    theServices = getServicesFromJson(jsonObjectString)
    if theServices is None:
        ####!!!!!!!  FIX ME  !!!!!!
        return buildInvalidInputErrorResponseJsonString(
                thisMessagingEntity=settings.WhoIAm,
                message="something went wrong trying to get the list of services")
    if theServices == []:
        log.debug("found services, but there are no keys.  Calling default")
        doDefaultService(jsonObjectString)
    log.debug("requestedServices: " + str(services))
    for requestedService in services:
        log.debug("requestedService: " + str(requestedService))
        if requestedService not in conjugateSettings.serviceModules.keys():
            theMessage="requested service not known to entity"
            log.error(theMessage)
            log.error("requested services: " + str(conjugateSettings.serviceModules.keys()))
            ## This could be made to be more specific - or not
            return buildInvalidInputErrorResponseJsonString(
                    thisMessagingEntity=settings.WhoIAm,
                    message=theMessage)
        # for now, send everything to glycoprotein builder.  This must change.
        returnedTransaction = glycoprotein.receive.receive(
                    jsonObjectString,
                    entityType=entityType)
        return returnedTransaction


def main():
  import importlib.util, os, sys
  #from importlib import util
  if importlib.util.find_spec("gemsModules") is None:
    this_dir, this_filename = os.path.split(__file__)
    sys.path.append(this_dir + "/../")
    if importlib.util.find_spec("common") is None:
      print("Something went horribly wrong.  No clue what to do.")
      return
    else:
      from common import utils
  else:
    from gemsModules.common import utils

  jsonObjectString=utils.JSON_From_Command_Line(sys.argv)
  returnedTransaction=receive(jsonObjectString)
  returnedTransaction.build_outgoing_string()
  return returnedTransaction.outgoing_string
  print(responseObjectString)


if __name__ == "__main__":
  main()

