#!/usr/bin/env python3
## Possibly this should be in gemsModules/project.

from abc import ABC, abstractmethod

from gemsModules.common.project_manager import Project_Manager

from gemsModules.{{cookiecutter.gems_module}}.main_api import {{cookiecutter.gems_module}}_Entity
from gemsModules.{{cookiecutter.gems_module}}.main_api_project import {{cookiecutter.gems_module}}_Project

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class {{cookiecutter.gems_module}}_Project_Manager(Project_Manager):

    def process(self) -> {{cookiecutter.gems_module}}_Project:
        self.response_project = {{cookiecutter.gems_module}}_Project()
        self.instantiate_response_project()
        return self.response_project

    def instantiate_response_project(self) -> {{cookiecutter.gems_module}}_Project:
        self.response_project.add_temporary_info()

    def fill_response_project_from_incoming_project(self):
        pass

    def fill_response_project_from_response_entity(self):
        pass


def testme() -> {{cookiecutter.gems_module}}_Project :
    the_entity={{cookiecutter.gems_module}}_Entity(type="{{cookiecutter.gems_module}}")
    the_project={{cookiecutter.gems_module}}_Project()
    the_manager={{cookiecutter.gems_module}}_Project_Manager(entity=the_entity, project=the_project)
    return the_manager.instantiate_new_project()

if __name__ == "__main__":
    project=testme()
    print(project.json(indent=2))
