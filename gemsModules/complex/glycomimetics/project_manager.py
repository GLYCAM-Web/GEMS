#!/usr/bin/env python3
## Possibly this should be in gemsModules/project.

from abc import ABC, abstractmethod
from pathlib import Path

from gemsModules.common.project_manager import Project_Manager

from gemsModules.complex.glycomimetics.main_api import Glycomimetics_Entity
from gemsModules.complex.glycomimetics.main_api_project import GlycomimeticsProject

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Glycomimetics_Project_Manager(Project_Manager):
    def process(self) -> GlycomimeticsProject:
        # log.debug("Glycomimetics_Project_Manager.process")
        # log.debug("incoming_entity: %s", self.incoming_entity)
        # log.debug("incoming_project: %s", self.incoming_project)
        
        self.instantiate_response_project()
        # Broken:
        # self.fill_response_project_from_incoming_project()
        self.fill_response_project_from_response_entity()

        return self.response_project

    def instantiate_response_project(self) -> GlycomimeticsProject:
        self.response_project = self.instantiate_new_project()

        return self.response_project

    @staticmethod
    def instantiate_new_project() -> GlycomimeticsProject:
        """This is a static method that returns a new project."""
        project = GlycomimeticsProject()
        project.add_temporary_info()
        return project

    # TODO: can probably be generalized and just pass the Project type.
    def fill_response_project_from_incoming_project(self):
        if self.incoming_project is not None:
            # need to combine instead of create new
            # self.response_project = GlycomimeticsProject(**self.incoming_project.dict())
            if self.response_project is None:
                self.response_project = self.instantiate_new_project()

            for key, value in self.incoming_project.dict().items():
                if key in self.response_project.dict().keys():
                    self.response_project.dict()[key] = value
                else:
                    log.warning("Key %s not in response project", key)

    def fill_response_project_from_response_entity(self):
        # TODO: incoming entity may be wrong to use here.
        log.debug("fill_response_project_from_response_entity %s", self.incoming_entity)

        # # Bad hack... # TODO: Ensure the IT fills inputs from resources before the PM? and ignore resources here?
        # inputs_needed = ["complex", "receptor", "ligand"]
        # for service in self.incoming_entity.services.__root__.values():
        #     log.debug("fill_response_project_from_response_entity %s", service)
        #     if hasattr(service.inputs, "complex_PDB_Filename"):
        #         self.response_project.complex = service.inputs.complex_PDB_Filename
        #         inputs_needed.remove("complex")
        #     if hasattr(service.inputs, "receptor_PDB_Filename"):
        #         self.response_project.receptor = service.inputs.receptor_PDB_Filename
        #         inputs_needed.remove("receptor")
        #     if hasattr(service.inputs, "ligand_PDB_Filename"):
        #         self.response_project.ligand = service.inputs.ligand_PDB_Filename
        #         inputs_needed.remove("ligand")
        #     if not len(inputs_needed):
        #         break

        # if len(inputs_needed):
        #     # Do we need to try to get from inputs.resources?
        #     # for resource in service.inputs.resources.__root__:
        #     #     if resource.resourceRole == "cocomplex":
        #     #         self.response_project.cocomplex = resource.payload
        #     #         inputs_needed.remove("cocomplex")
        #     #     elif resource.resourceRole == "moiety":
        #     #         self.response_project.moiety = resource.payload
        #     #         inputs_needed.remove("moiety")
        #     #     if not len(inputs_needed):
        #     #         break
        #     log.warning(f"Could not find all inputs: {inputs_needed}. ")


def testme() -> GlycomimeticsProject:
    the_entity = Glycomimetics_Entity(type="Glycomimetics")
    the_project = Glycomimetics_Entity()
    the_manager = Glycomimetics_Project_Manager(
        entity=the_entity, incoming_project=the_project
    )
    return the_manager.instantiate_new_project()


if __name__ == "__main__":
    project = testme()
    print(project.json(indent=2))
