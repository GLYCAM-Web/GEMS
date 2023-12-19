#!/usr/bin/env python3
from enum import Enum
from gemsModules.common.code_utils import GemsStrEnum

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Known_Entities(GemsStrEnum):
    """
    The entities that Delegator knows about.
    """

    Delegator = "Delegator"
    DeprecatedDelegator = "DeprecatedDelegator"
    MDaaS = "MDaaS"
    Status = "Status"
    BatchCompute = "BatchCompute"
    Conjugate = "Conjugate"
    CommonServices = "Common"
    MmService = "MmService"
    Query = "Query"
    Sequence = "Sequence"
    DrawGlycan = "DrawGlycan"
    StructureFile = "StructureFile"
    PDBFile = "PDBFile"


from gemsModules.deprecated import delegator as deprecated_delegator
from gemsModules.batchcompute import slurm
from gemsModules import common
from gemsModules.mmservice import mdaas
from gemsModules import mmservice
from gemsModules.structurefile import PDBFile
from gemsModules import status

Known_Entity_Modules = {
    "MDaaS": mdaas,
    "MmService": mmservice,
    "Status": status,
    "BatchCompute": slurm,
    "PDBFile": PDBFile,
}
