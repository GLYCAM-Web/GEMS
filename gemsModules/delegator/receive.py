#!/usr/bin/env python3
import gemsModules
from datetime import datetime
from gemsModules import common
import gemsModules.common.logic as commonLogic # replacing services
from gemsModules.delegator import settings
#import gemsModules.common.common_api as commonIO # replacing transaction
import gemsModules.delegator.delegator_api as delegatorIO # replacing transaction
from gemsModules.common.loggingConfig import *
import traceback

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

def receive(jsonObjectString):
    """
    Call other modules based on the contents of jsonObjectString.

    Returns a JSON object in string form.  Can be pretty-printed.

    First, a new Transaction obect is made.  This object holds all the
    information about the delegated work.  To initialize it, we give it
    the incoming JSON object, which is then interrogated by parseInput
    in the common.services module.  If that goes well, this function
    reads the identity of the top-level Entity and, if it can load a
    module for that entity, it passes the Transaction object over.
    """

    log.info("delegate() was called.\n")
    log.debug("incoming jsonObjectString: " + jsonObjectString)   
    log.debug("calling commonIO.Transaction")
    try:
        log.debug("trying to instantiate Transaction")  
        #thisTransaction = commonIO.Transaction()
        thisTransaction = delegatorIO.Transaction()
        response_code = thisTransaction.process_incoming_string(
            in_string = jsonObjectString,  
            no_check_fields = True, 
            initialize_out = False 
            )
        if response_code != 0 :
            thisTransaction.generate_error_response(Brief='GemsError', EntityType=settings.WhoIAm)
            return thisTransaction.get_outgoing_string()
    except Exception as error:
        errorMessage = ("problem instantiating Transaction from string: " + str(jsonObjectString))
        log.error(errorMessage)
        log.error(traceback.format_exc())

    
    if thisTransaction.transaction_in.entity.entityType == settings.WhoIAm :
        thisTransaction.process()
    else :
        try:
            import gemsModules.common.logic as logic_importEntity
            theEntity = logic_importEntity(entityType)
            log.debug("theEntity: " + str(theEntity))
        except Exception as error:
            error_msg = "There was a problem importing the entity: " + str(error)
            log.error(error_msg)
            log.error(traceback.format_exc())
            thisTransaction.generateCommonParserNotice(messagingEntity='delegator', additionalInfo={"errorMessage":error_msg})

    return thisTransaction.outgoing_string


##  Return the content of the current schema, as defined in CurrentStableSchema
def getJsonSchema():
    log.info("getJsonSchema() was called.\n")
    #versionFilename = getGemsHome() + "/gemsModules/Schema/currentStableSchema"
    versionFilename = commonLogic.getGemsHome() + "/gemsModules/Schema/currentStableSchema"
    with open(versionFilename, 'r') as versionFile:
        currentStableVersion = versionFile.read().strip()
    #schemaFileName = getGemsHome() + "/gemsModules/Schema/" + currentStableVersion + "/schema.json"
    schemaFileName = commonLogic.getGemsHome() + "/gemsModules/Schema/" + currentStableVersion + "/schema.json"
    with open(schemaFileName, 'r') as schemaFile:
        content = schemaFile.read()
    #log.debug("schema content: \n" + content )
    return content

def main():
    # 
    import importlib.util, os, sys
    if importlib.util.find_spec("gemsModules") is None:
        this_dir, this_filename = os.path.split(__file__)
        sys.path.append(this_dir + "/../")
        if importlib.util.find_spec("common") is None:
            print("I cannot find the Common Servicer.  No clue what to do. Exiting")
            sys.exit(1)
        else:
            from common import utils
    else:
        from gemsModules.common import utils
        jsonObjectString=utils.JSON_From_Command_Line(sys.argv)

    try:
        responseObjectString=receive(jsonObjectString)
    except IndexError as error:
        print("\nlength of argv: " + str(len(sys.argv)))
        print("at least one json formatted string argument is required\n")
        responseObject = {
            'DelegatorNotice' : {
                'type' : 'IndexError',
                'notice' : {
                    'code' : '500',
                    'brief' : 'No json input string!',
                    'noticeType' : 'Error',
                    'message' : 'Delegator requires a json formatted string as input.',
                    'scope' : 'Delegator',
                    'messenger' : 'Delegator'
                    }
                }
            }
        responseObjectString = str(responseObject)

    except Exception as error:
        print("\nThe delegator module captured an error.")
        print("Error type: " + str(type(error)))
        print(traceback.format_exc())

        responseObject = {
            'DelegatorNotice' : {
                'type' : 'UnknownError',
                'notice' : {
                    'code' : '500',
                    'brief' : 'unknownError',
                    'message' : 'Not sure what went wrong. Error captured by the Delegator gemsModule.',
                    'noticeType' : 'Error',
                    'scope' : 'Delegator',
                    'messenger' : 'Delegator'
                    }
                }
            }  
        responseObjectString = str(responseObject)

    print("\ndelegator is returning this: \n" +  str(responseObjectString))

if __name__ == "__main__":
    main()

