import sys, os, re, importlib.util
import gemsModules
import gmml
from gemsModules.common.services import *
from gemsModules.common.transaction import * # might need whole file...
from gemsModules.common.loggingConfig import *
from . import settings
from . import statusResponse
from datetime import datetime
import traceback

##TO set logging verbosity for just this file, edit this var to one of the following:
## logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
logLevel = logging.ERROR

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__, logLevel)

def receive(thisTransaction : Transaction):
    log.info("receive() was called.\n")

    if not 'services' in thisTransaction.request_dict['entity'].keys():
        log.debug("'services' was not present in the request. Do the default.")
        doDefaultService(thisTransaction)
        return
    else:
        services = getTypesFromList(thisTransaction.request_dict['entity']['services'])
        for requestedService in services:
            log.debug("requestedService: " + str(requestedService))
            if requestedService not in settings.serviceModules.keys():
                if requestedService not in common.settings.serviceModules.keys():
                    log.error("The requested service is not recognized.")
                    common.settings.appendCommonParserNotice( thisTransaction, 'ServiceNotKnownToEntity', requestedService)
            elif requestedService == "GenerateReport":
                generateReport(thisTransaction, None)
                thisTransaction.build_outgoing_string()
            else:
                log.error("Perhaps a service was added to status/settings.py, but not defined in receive.py? Likely this service is still in development.")
                common.settings.appendCommonParserNotice( thisTransaction, 'ServiceNotKnownToEntity', requestedService)

##This method needs to check for options. If options are not present, do the default service.
##    If the options are present, and specify a list of entities to report on, only report on those.
def generateReport(thisTransaction : Transaction, thisService : Service = None):
    log.info("generateReport() was called.\n")

    entityKeys = thisTransaction.request_dict['entity'].keys()
    log.debug("entityKeys : " + str(entityKeys))

    if 'options' in entityKeys:
        optionsKeys = thisTransaction.request_dict['entity']['options'].keys()
        options = thisTransaction.request_dict['entity']['options']
        log.debug("optionsKeys: " + str(optionsKeys))
        if "targets" in optionsKeys:
            for target in options['targets']:
                log.debug("Report requested for target: " + str(target))
                log.debug("target type: " + str(target['type']))
                if target['type'] == 'All':
                    doDefaultService(thisTransaction)
                else:
                    log.error("Report requested for a specific target. Still being developed.")
                    ##TODO: Add an error to common parser to return to frontend. reportTargetUnknown
        else:
            doDefaultService(thisTransaction)

    else:
        doDefaultService(thisTransaction)

##TODO: Refactor for better encapsulation
## The default here is to just report on every gemsModule and their corresponding services.
def doDefaultService(thisTransaction : Transaction):
    log.info("doDefaultService() was called.\n")
    #log.debug("thisTransaction: " + str(thisTransaction))

    ##Header section
    if thisTransaction.response_dict is None:
        thisTransaction.response_dict = {}

    thisTransaction.response_dict['entity'] = {}
    thisTransaction.response_dict['entity']['type']="StatusReport"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    log.debug("timestamp: " + str(timestamp))

    thisTransaction.response_dict['entity']['timestamp'] = timestamp
    responses = []
    ##Entity Reporting
    entities = listEntities()
    log.debug("entities: " + str(entities) + "\n")
    for availableEntity in entities:
        log.debug("Generating a report for entity: " + availableEntity)
        response = {}
        thisEntity = importEntity(availableEntity)
        response.update({
            'entity' : availableEntity
        })
        log.debug("thisEntity.__dict__.keys(): " + str(thisEntity.__dict__.keys()))
        if thisEntity.settings is not None:
            settings = thisEntity.settings
            settingsAttributes = settings.__dict__.keys()

            response = getModuleStatus(response, settings, settingsAttributes)
            response = getModuleStatusDetail(response, settings, settingsAttributes)
            response = getServiceStatuses(response, settings, settingsAttributes)
            response = getSubEntities(response, settings, settingsAttributes)

            log.debug("Type of response: " + str(type(response)))
            log.debug("response: " + str(response))
            responses.append(response)

        else:
            log.error("Could not find settings for this entity.")
            ##TODO: Add an error to common parser for settingsNotFound

    thisTransaction.response_dict.update({
        "responses": responses
    })
    #log.debug("thisTransaction.response_dict: " + str(thisTransaction.response_dict))

##Append a status from a module's settings file to a json response object
def getModuleStatus(response, settings, settingsAttributes):
    log.info("getModuleStatus() was called.\n")
    if 'status' in settingsAttributes:
        status = settings.status
        log.debug("settings.status: " + status)
        response.update({
            'status' : status
        })
    return response

##Append a module status detail from a module's settings file to a json response object
def getModuleStatusDetail(response, settings, settingsAttributes):
    log.info("getModuleStatusDetail() was called.\n")
    if 'moduleStatusDetail' in settingsAttributes:
        moduleStatusDetail = settings.moduleStatusDetail
        log.debug("settings.moduleStatusDetail: " + moduleStatusDetail)
        response.update({
            'moduleStatusDetail' : moduleStatusDetail
        })
    return response

##Append a list of module services and their statuses to a json response object
def getServiceStatuses(response, settings, settingsAttributes):
    log.info("getServiceStatuses() was called.\n")
    if 'servicesStatus' in settingsAttributes:
        serviceStatuses= []
        for element in settings.servicesStatus:
            service = element['service']
            log.debug("service: " + service)
            serviceStatus = element['status']
            log.debug("serviceStatus: " + str(serviceStatus))
            serviceStatusDetail = element['statusDetail']
            log.info("statusDetail: " + serviceStatusDetail)
            serviceStatuses.append(element)

        response.update({
            'services' : serviceStatuses
        })
    return response

##Update a response with the entities an entity uses.
def getSubEntities(response, settings, settingsAttributes):
    log.info("getSubEntities() was called.\n")
    if 'subEntities' in settingsAttributes:
        subEntities = []
        for subEntity in settings.subEntities:
            log.debug("subEntity: " + str(subEntity))
            subEntities.append(subEntity)

        response.update({
            'subEntities' : subEntities
        })
    return response

def main():
    ## TODO:  Make this look more like the main in delegator's receive.py
    GemsPath = os.environ.get('GEMSHOME')
    if GemsPath == None:
        this_dir, this_filename = os.path.split(__file__)
        print("""

        GEMSHOME environment variable is not set.

        Set it using somthing like:

          BASH:  export GEMSHOME=/path/to/gems
          SH:    setenv GEMSHOME /path/to/gems
        """)

    #print("length of argv: " + str(len(sys.argv)))
    if len(sys.argv) > 1:
        #print("looking for the input filename.")
        if os.path.isfile(sys.argv[1]):
            inputFile = sys.argv[1]
        else:
            #print("got an arg that is not a filename: " + sys.argv[1])
            inputFile = GemsPath + "/gemsModules/delegator/test_in/statusReport_All.json"
    else:
        #print("no argv was offered.")
        inputFile = GemsPath + "/gemsModules/delegator/test_in/statusReport_All.json"

    #print("using the default inputFile: " + inputFile)
    #print(os.listdir("../../delegator/test_in/"))

    with open(inputFile, 'r') as file:
        jsonObjectString = file.read().replace('\n', '')
        #print("jsonObjectString: " + str(jsonObjectString))

    #Create transaction, then pass that to receive
    thisTransaction = Transaction(jsonObjectString)

    try:
        parseInput(thisTransaction)
    except Exception as error:
        print("Error parsing input.")
        print("Error type: " + str(type(error)))
        print(traceback.format_exc())

    receive(thisTransaction)

    responseObjectString = thisTransaction.outgoing_string
    return responseObjectString

if __name__ == "__main__":
    main()
