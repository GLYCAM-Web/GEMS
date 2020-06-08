#!/usr/bin/env python3
import  os, sys
import json
import uuid
from datetime import datetime
from gemsModules.common.services import *
from gemsModules.project import settings as project_settings
from pydantic import BaseModel, Field, ValidationError
from pydantic.schema import schema
from gemsModules.common.loggingConfig import *
import traceback

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


##  @brief The primary way of tracking data related to a project
#   @detail This is the generic project object. See subtypes for more specific fields
class GemsProject(BaseModel):
    ## The name of the output dir is the pUUID
    pUUID : str = ""
    title : str = ""
    comment : str = ""
    timestamp : datetime = None
    project_type : str = ""

    ## The project path. Used to be output dir, but now that is reserved for subdirs.
    project_dir : str = ""
    requesting_agent : str = ""
    has_input_files : bool = None
    gems_version : str = ""
    gems_branch : str = ""
    gmml_version : str = ""
    gmml_branch : str = ""
    site_mode : str = ""
    site_host_name : str = ""
    force_field : str = ""
    parameter_version : str = ""
    amber_version : str = ""
    json_api_version : str = ""
    
    

    def __init__(self, request_dict : dict):
        super().__init__()
        log.info("GemsProject.__init__() was called.")
        log.debug("request_dict: " + str(request_dict))

        ## Random uuid for the project uuid.
        self.pUUID = str(uuid.uuid4()) 
        self.timestamp = datetime.now()

        if 'project' in request_dict.keys():
            log.debug("found a project in the request_dict.")
            fe_project = request_dict['project']
            
            if 'title' in fe_project.keys():
                self.title = fe_project['title']
            if 'comment' in fe_project.keys():
                self.comment = fe_project['comment']
            if 'requesting_agent' in fe_project.keys():
                self.requesting_agent = fe_project['requesting_agent']
            if 'gems_version' in fe_project.keys():
                self.gems_version = fe_project['gems_version']
            if 'gems_branch' in fe_project.keys():
                self.gems_branch = fe_project['gems_branch']
            if 'gmml_version' in fe_project.keys():
                self.gmml_version = fe_project['gmml_version']
            if 'gmml_branch' in fe_project.keys():
                self.gmml_branch = fe_project['gmml_branch']
            if 'site_mode' in fe_project.keys():
                self.site_mode = fe_project['site_mode']
            if 'site_host_name' in fe_project.keys():
                self.site_host_name = fe_project['site_host_name']
            if 'force_field' in fe_project.keys():
                self.force_field = fe_project['force_field']
            if 'parameter_version' in fe_project.keys():
                self.parameter_version =  fe_project['parameter_version']
            if 'amber_version' in fe_project.keys():
                self.amber_version = fe_project['amber_version']
            if 'json_api_version' in fe_project.keys():
                self.json_api_version = fe_project['json_api_version']
        else:
            ##  In a commandline request, a frontend project may not be included.
            #   This is where we give defaults for whatever is needed.
            self.requesting_agent = "command line"
            log.debug("request entity type: " + request_dict['entity']['type'])
            if request_dict['entity']['type'] == "Sequence":
                self.project_type = "cb"
                self.has_input_files = False
            elif request_dict['entity']['type'] == "MmService":
                self.project_type = "md"
                self.has_input_files = True
            elif request_dict['entity']['type'] == "Conjugate":
                self.project_type = "gp"
                self.has_input_files = True
            elif request_dict['entity']['type'] == "StructureFile":
                self.project_type = "pdb"
                self.has_input_files = True

          
            
    def __str__(self):
        result = "\ngems_project:"
        result = result + "\ncomment: " + self.comment
        result = result + "\ntimestamp: " + str(self.timestamp)
        result = result + "\nproject_type: " + self.project_type
        result = result + "\npUUID: " + self.pUUID
        result = result + "\nrequesting_agent: " + self.requesting_agent
        result = result + "\nhas_input_files: " + str(self.has_input_files)
        result = result + "\ngems_version: "  + self.gems_version
        result = result + "\ngems_branch: "  + self.gems_branch
        result = result + "\ngmml_version: "  + self.gmml_version
        result = result + "\ngmml_branch: "  + self.gmml_branch
        result = result + "\nsite_mode: "  + self.site_mode
        result = result + "\nsite_host_name: "  + self.site_host_name
        result = result + "\nforce_field: "  + self.force_field
        result = result + "\nparameter_version: "  + self.parameter_version
        result = result + "\namber_version: "  + self.amber_version
        result = result + "\njson_api_version: "  + self.json_api_version
        return result



## @brief cbProject is a typed project that inherits all the fields from gems_project and adds its own.
#   
class CbProject(GemsProject):
    sequence : str = ""
    seqID : str = ""
    structure_count : int = 1
    #structure_mappings : []

    def __init__(self, request_dict: dict):
        super().__init__(request_dict)
        log.info("CbProject.__init__() was called.")
        from gemsModules.project.projectUtil import getSequenceFromTransaction, getSeqIDForSequence
        self.project_type = "cb"
        inputs = request_dict['entity']['inputs']
        sequence = ""
        for element in inputs:
            if "Sequence" not in element.keys():
                sequence = element['Sequence']['payload']
        if sequence is not "":
            self.sequence = sequence
            self.seqID = getSeqIDForSequence(sequence)
        inputs = request_dict['entity']['inputs']
        requested_structure_count = 0
        for element in inputs:
            if 'Sequence' in element.keys():
                requested_structure_count = requested_structure_count + 1
        structure_count = requested_structure_count

        self.project_dir = project_settings.output_data_dir + "tools/" +  self.project_type  + "/git-ignore-me_userdata/" + self.pUUID + "/" 

    def __str__(self):
        result = super().__str__()
        result = result + "\nproject_type: " + self.project_type
        result = result + "\nsequence: " + self.sequence
        result = result + "\nseqID: " + self.seqID
        result = result + "\nstructure_count: " + str(self.structure_count)
        #result = result + "\nstructure_mappings: " + str(self.structure_mappings)
        return result

class PdbProject(GemsProject):
    uploadFileName : str = ""
    status : str = ""

    def __init__(self, request_dict: dict):
        super().__init__(request_dict)
        from gemsModules.structureFile.amber.receive import getInput
        log.info("PdbProject.__init__() was called.")
        self.project_type = "pdb"
        self.has_input_files = True
        self.uploadFileName = getInput(request_dict)
        log.debug("uploadFileName: " + self.uploadFileName)
        self.status = "submitted"
        self.project_dir = project_settings.output_data_dir + "tools/" +  self.project_type  + "/git-ignore-me_userdata/" + self.pUUID + "/" 

    def __str__(self): 
        result = super().__str__()
        result = result + "\nproject_type: " + self.project_type
        result = result + "\nuploadFileName: " + self.uploadFileName
        result = result + "\nstatus: " + self.status
        return result


class GpProject(GemsProject):
    pdbProjectID : str = ""
    uploadFileName : str = ""
    status : str = ""

    def __init__(self, request_dict : dict):
        super().__init__(request_dict)
        log.info("GpProject.__init__() was called.")
        pdbProject = PdbProject(request_dict)
        log.debug("pdbProject: \n" + str(pdbProject.__dict__))
        self.pdbProjectID = pdbProject.pUUID
        self.status = "submitted"
        self.project_type = "gp"
        self.has_input_files = True
        self.uploadFileName = pdbProject.uploadFileName
        self.project_dir = project_settings.output_data_dir + "tools/" +  self.project_type  + "/git-ignore-me_userdata/" + self.pUUID + "/" 
 

    def __str__(self):
        result = super().__str__()
        result = result + "\npdbProjectId: " + self.pdbProjectID
        result = result + "\nstatus: " + self.status
        return result


## Details and location of the build of a single pose of a structure.
class StructureMapping():
    ##  Path to the dir that holds this build. 
    #   May or may not be in this project dir.
    structure_path : str = ""
    ion : str = "No"
    solvation : str = "No"
    solvation_size : str = ""
    solvation_distance : str = ""
    splvation_shape : str = "REC"
    timestamp : str = None

##  Figures out the type of structure file being preprocessed.
def getStructureFileProjectType(request_dict):
    projectType = "not set"
    services = request_dict['entity']['services']
    for service in services:
        if 'Preprocess' in service.keys():
            if 'type' in service['Preprocess'].keys():
                if 'PreprocessPdbForAmber' == service['Preprocess']['type']:
                    projectType = "pdb"

    return projectType

##TODO: pydantic homework when model has settled down.

# def generategems_projectSchema():
#     print(gems_project.schema_json(indent=2))

if __name__ == "__main__":
    generategems_projectSchema()
