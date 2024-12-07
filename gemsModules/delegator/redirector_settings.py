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
    CommonServicer = "CommonServicer"
    MmService = "MmService"
    Query = "Query"
    Sequence = "Sequence"
    DrawGlycan = "DrawGlycan"
    StructureFile = "StructureFile"
    PDBFile = "PDBFile"
    Glycomimetics = "Glycomimetics"


from gemsModules.deprecated.delegator.receive import delegate as deprecated_delegator

# TODO: For now, amber is directly calling slurm, rather than going through delegator.
# Part of the reason for this is that the grpc_slurm_server does not expect a full GEMS request, but a slurm job submission dict.
# from gemsModules.batchcompute.slurm.receive import receive as slurm
from gemsModules.common.receive import receive as common

from gemsModules.mmservice.receive import receive as mmservice
from gemsModules.mmservice.mdaas.receive import receive as mdaas

from gemsModules.structurefile.PDBFile.receive import receive as pdbfile
from gemsModules.status.receive import receive as status

from gemsModules.complex.glycomimetics.receive import receive as glycomimetics


Known_Entity_Reception_Modules = {
    #'BatchCompute' : batchcompute,  for now, still deprecated
    "CommonServicer": common,
    "MDaaS": mdaas,
    "MmService": mmservice,
    "Status": status,
    # Deprecated
    "BatchCompute": deprecated_delegator,
    "Conjugate": deprecated_delegator,
    "Delegator": deprecated_delegator,
    "DeprecatedDelegator": deprecated_delegator,
    "DrawGlycan": deprecated_delegator,
    "Query": deprecated_delegator,
    "Sequence": deprecated_delegator,
    #'Status' : deprecated_delegator,
    "StructureFile": deprecated_delegator,
    "PDBFile": pdbfile,
    "Glycomimetics": glycomimetics,
}
