#!/usr/bin/env python3
import sys, os, re, importlib.util
import gemsModules
#from gemsModules import common
#from gemsModules import sequence
#from gemsModules.sequence.entity import *
from gemsModules.common.services import *
from gemsModules.common.transaction import * # might need whole file...
from . import settings

## TODO Write this function
def evaluate(thisTransaction : Transaction, thisService : Service = None):
    # from .evaluate import *
    #if ('jsonObjectOutputFormat', 'Pretty') in self.transaction_in.options:
    # evaluateSequenceSanity(thisTransaction : Transaction)
    print("evaluate was called! ...But it has not been written for this module yet.")

def build3DStructure(thisTransaction : Transaction, thisService : Service = None):
    print("~~~ Sequence entity's build3Dstructure was called!")
    import uuid
    theUUID=str(uuid.uuid4())

    inputs = thisTransaction.request_dict['entity']['inputs']
    theInputs=getTypesFromList(inputs)
    if 'Sequence' in theInputs: 
        print("found Sequence in theInputs")
    else:
        #sequence is required. Attach an error response and return.
        common.settings.appendCommonParserNotice(thisTransaction,'ServiceNotKnownToEntity','Expected Sequence')
        return

    ### This is REALLY REALLY UGLY  PLEASE FIX THIS
    theSequence=list(list(inputs[0].values())[0].values())[0]
    #print(theSequence)

    ## The original way. TODO: delete the subprocess call to the bash file.
    import subprocess
    subprocess.run("$GEMSHOME/gemsModules/sequence/do_the_build.bash '" + theSequence +"' " + theUUID, shell=True)
    print("Attempting to do the build.")
    
    # try:
    #     print("Attempting to doTheBuild()")
    #     doTheBuild(theSequence, theUUID)
    # except Exception as error:
    #     print("There was an error while attempting to doTheBuild.")
    #     print("Error type: " + str(type(error)))
    #     print("Error details: " + str(error))
        

    if thisTransaction.response_dict is None:
        thisTransaction.response_dict={}
    if not 'entity' in thisTransaction.response_dict:
        thisTransaction.response_dict['entity']={}
    if not 'type' in thisTransaction.response_dict['entity']:
        thisTransaction.response_dict['entity']['type']='Sequence'
    if not 'responses' in thisTransaction.response_dict:
        thisTransaction.response_dict['responses']=[]

    thisTransaction.response_dict['responses'].append({'Build3DStructure': {'payload': theUUID }})


def doDefaultService(thisTransaction : Transaction):
    # evaluate(thisTransaction : Transaction)
    # build3DStructure(thisTransaction : Transaction)
    if thisTransaction.response_dict is None:
        thisTransaction.response_dict={}
    thisTransaction.response_dict['entity']={}
    thisTransaction.response_dict['entity']['type']='SequenceDefault'
    thisTransaction.response_dict['responses']=[]
    thisTransaction.response_dict['responses'].append({'DefaultTest': {'payload':marco('Sequence')}})
    thisTransaction.build_outgoing_string()

def receive(thisTransaction : Transaction):
    print("~~~\nSequence entity has received a transaction.")
    import gemsModules.sequence
    ## First figure out the names of each of the requested services
    if not 'services' in thisTransaction.request_dict['entity'].keys():
        print("'services' was not present in the request. Do the default.")
        doDefaultService(thisTransaction)
        return

    input_services = thisTransaction.request_dict['entity']['services']
    theServices=getTypesFromList(input_services)

    ## for each requested service
    for i in theServices:
        #####  the automated module loading doesn't work, and I can't figure out how to make it work,
              # that is:
              #  requestedModule='.'+settings.serviceModules[i]
              #  the_spec = importlib.util.find_spec('.sequence.entity.evaluate',gemsModules)
              # .... and many variants thereof
        #####  so, writing something ugly for now
        if i not in settings.serviceModules.keys():
            if i not in common.settings.serviceModules.keys():
                print("The provided service is not recognized. Building and returning an error response.")
                common.settings.appendCommonParserNotice( thisTransaction,'ServiceNotKnownToEntity',i)
            else:
                pass

        ## if it is known, try to do it
        elif i == "Evaluate":
            evaluate(thisTransaction,  None)
        elif i == 'Build3DStructure':
            build3DStructure(thisTransaction ,  None)
        else:
            print("got to the else, so something is wrong")
            common.settings.appendCommonParserNotice( thisTransaction,'ServiceNotKnownToEntity',i)
    thisTransaction.build_outgoing_string()
            


# Some alternate ways to interrogate lists:
#    if any("Evaluate" in s for s in input_services ):
#        print("It is here!")
#    types=[s for s in input_services if "type" in s.values()]
#    evaluations=[s for s in input_services if "Evaluate" in s]
#    print(evaluations)


def main():
    pass

if __name__ == "__main__":
  main()
 
