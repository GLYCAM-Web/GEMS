#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List
from pathlib import Path

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.request_data_filler import Request_Data_Filler
from gemsModules.common.main_api_resources import Resource

from gemsModules.complex.glycomimetics.main_api import Glycomimetics_Entity
from gemsModules.complex.glycomimetics.main_api_project import GlycomimeticsProject

from .Build_Selected_Positions import api as build_api
from .ProjectManagement import api as pm_api
from .Evaluate import api as evaluate_api
from .Validate import api as validate_api

from gemsModules.common.code_utils import find_aaop_by_id

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Glycomimetics_Request_Data_Filler(Request_Data_Filler):
    def process(self) -> list[AAOP]:
        """Fill in any data required in the service request aaop_list."""
        
        # We will fill all AAOPs in order, ensuring PM aaop exists before we depend on project paths.
        update_proj_dirs = []
        do_proj_dir_update = False
        for i, aaop in enumerate(self.aaop_list):
            log.debug(f"i: {i}, {aaop.AAO_Type}={aaop}")

            if aaop.AAO_Type == "Build_Selected_Positions":
                self.__fill_build_aaop(i, aaop)
                update_proj_dirs.append(aaop)
            elif aaop.AAO_Type == "ProjectManagement":
                self.__fill_projman_aaop(i, aaop)
                do_proj_dir_update = True
            elif aaop.AAO_Type == "Evaluate":
                self.__fill_evaluate_aaop(i, aaop)
                update_proj_dirs.append(aaop)
            elif aaop.AAO_Type == "Validate":
                self.__fill_validate_aaop(i, aaop)
                update_proj_dirs.append(aaop)
            else:
                log.warning(f"GM/RequestDataFiller: I don't know how to data fill for {aaop.AAO_Type}")

        if not do_proj_dir_update:
            log.warning("GM/RequestDataFiller: No ProjectManagement AAOP found to update project directories.")
            log.warning("This WILL cause problems with the service execution.")
        else:   
            self.__post_process_fill(update_proj_dirs)

        return self.aaop_list

    def __post_process_fill(self, update_proj_dirs: List[AAOP]):
        # TODO/FIX: Hack, but easiest/cheapest way to get all project resources to have the project_dir prepended.
        roles_to_find = ["Complex", "Ligand", "Receptor"]
        for aaop in update_proj_dirs:
            log.debug(f"GM/RequestDataFiller: Prepending project_dir to resources for {aaop.AAO_Type}")
            for r in aaop.The_AAO.inputs.resources:
                if not roles_to_find:
                    return True
                if (
                    r.resourceRole in roles_to_find
                    and r.locationType == "filesystem-path-unix"
                ):
                    # extract filename from payload
                    r.payload = str(Path(self.response_project.project_dir) / Path(r.payload).name)
                    log.debug(
                        f"GM/RequestDataFiller: {r.resourceRole} prepended project_dir to Receptor payload: {r.payload}"
                    )
                    
                    roles_to_find.remove(r.resourceRole)
                    break
        
        if roles_to_find:
            log.warning(f"GM/RequestDataFiller: Could not find resources for roles: {roles_to_find}")
        return False
    
    def __fill_build_aaop(self, i: int, aaop: AAOP) -> List[AAOP]:
        # Please note, if you need values from response_project, make sure they are initialized appropriately by project manager.

        aaop.The_AAO.inputs.pUUID = self.response_project.pUUID
        # aaop.The_AAO.inputs.projectDir = self.response_project.project_dir
        # aaop.The_AAO.inputs.outputDirPath = self.response_project.project_dir

        complex_filename, ligand_filename, receptor_filename = None, None, None

        # TODO: need a helper for this / TODO: Validate and Evaluate need to work directly.
        if aaop.The_AAO.inputs.complex_PDB_Filename:
            complex_filename = aaop.The_AAO.inputs.complex_PDB_Filename
        else:
            complex_filename = self.response_project.complex
        if aaop.The_AAO.inputs.ligand_PDB_Filename:
            ligand_filename = aaop.The_AAO.inputs.ligand_PDB_Filename
        else:
            ligand_filename = self.response_project.ligand
        if aaop.The_AAO.inputs.receptor_PDB_Filename:
            receptor_filename = aaop.The_AAO.inputs.receptor_PDB_Filename
        else:
            receptor_filename = self.response_project.receptor

        if complex_filename:
            pdb = Resource(
                payload=complex_filename,
                resourceFormat="chemical/pdb",
                resourceRole="Complex",
                locationType="filesystem-path-unix",
            )
            aaop.The_AAO.inputs.resources.add_resource(pdb)
        if ligand_filename:
            pdb = Resource(
                payload=ligand_filename,
                resourceFormat="chemical/pdb",
                resourceRole="Ligand",
                locationType="filesystem-path-unix",
            )
            aaop.The_AAO.inputs.resources.add_resource(pdb)
        if receptor_filename:
            pdb = Resource(
                payload=receptor_filename,
                resourceFormat="chemical/pdb",
                resourceRole="Receptor",
                locationType="filesystem-path-unix",
            )
            aaop.The_AAO.inputs.resources.add_resource(pdb)

        return self.aaop_list

    def __fill_projman_aaop(self, i: int, aaop: AAOP):
        aaop.The_AAO.inputs.pUUID = self.response_project.pUUID
        aaop.The_AAO.inputs.projectDir = self.response_project.project_dir

        # Add the resources to copy to the project output directory by the Project Management service.
        # TODO: copy parm7/rst7 this way.
        input_json = pm_api.PM_Resource(
            payload=self.transaction.incoming_string,
            resourceFormat="json",
            locationType="Payload",
            options={"filename": "request.json"},
        )
        aaop.The_AAO.inputs.resources.add_resource(input_json)

        # TODO: need to handle the case of direct inputs that are not resources.
        self.fill_resources_from_requester_if_exists(aaop, deep_copy=True)

    def __fill_evaluate_aaop(self, i: int, aaop: AAOP) -> List[AAOP]:
        aaop.The_AAO.inputs.pUUID = self.response_project.pUUID

        # TODO: need to handle the case of direct inputs that are not resources.
        self.fill_resources_from_requester_if_exists(aaop)
        # Add the resources to copy to the project output directory by the Project Management service.

    def __fill_validate_aaop(self, i: int, aaop: AAOP) -> List[AAOP]:
        aaop.The_AAO.inputs.pUUID = self.response_project.pUUID

        # TODO: need to handle the case of direct inputs that are not resources.
        self.fill_resources_from_requester_if_exists(aaop)