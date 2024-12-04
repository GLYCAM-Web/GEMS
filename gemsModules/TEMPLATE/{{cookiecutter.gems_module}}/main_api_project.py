#!/usr/bin/env python3
from typing import Literal
import os

from pydantic import constr, Field

from gemsModules.project.main_api import Project

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class {{cookiecutter.gems_module}}_Project(Project):
    """ {{cookiecutter.gems_module}} project for making new entities. """
    title : str = "{{cookiecutter.gems_module}} project"
    parent_entity : str = ""
    app : str = "{{cookiecutter.gems_module}}"
    requested_service : str = "{{cookiecutter.service_name}}"
    entity_id : str = "{{cookiecutter.gems_module}}"
    service_id : str = "{{cookiecutter.service_name}}"
    filesystem_path : str = "/some/path/"
    service_dir : str = "{{cookiecutter.service_name}}_dir"
    requesting_agent : str = ""
    has_input_files : bool = True
    u_uuid : constr(max_length=36) = " "
    notify : bool = False
    upload_path : constr(max_length=255)  = "/path/to/{{cookiecutter.service_name}}_dir"
    
    project_type : Literal['{{cookiecutter.gems_module}}'] = Field(  
            '{{cookiecutter.gems_module}}',
            title='Type',
            alias='type'
            )

    def add_temporary_info(self): 
        self.project_dir : str = os.path.join(self.filesystem_path,
                self.service_dir,
                self.project_type,
                self.pUUID)
        self.compute_cluster_filesystem_path : str = self.project_dir
        self.logs_dir : str = os.path.join(self.project_dir, "logs")
        self.site_mode : str = "proof-of-concept"
        self.versions_file_path : str = os.path.join(self.project_dir, "VERSIONS.sh")