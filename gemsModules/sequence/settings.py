#!/usr/bin/env python3
from gemsModules.common.utils import GemsStrEnum
from sequence.build_3D_servicer import build3DStructure
from sequence.evaluate_servicer import evaluate
from sequence.status_servicer import get_status
from sequence.evaluate_servicer import validate
from sequence.status_servicer import get_status
from enum import Enum

# Who I am
WhoIAm = 'Sequence'

# Status Report
status = "Stable"
moduleStatusDetail = "Nearing ready for v1 release. Needs tests and documentation."

servicesStatus = [
    {
        "service": "Validate",
        "status": "Stable.",
        "statusDetail": "Rarely used Evaluate includes Validate. Validate mayeventually be deprecated."
    },
    {
        "service": "Evaluate",
        "status": "Stable.",
        "statusDetail": "Works for GLYCAM condensed sequences."
    },
    {
        "service": "Build3DStructure",
        "status": "Stable.",
        "statusDetail": "Ready for tests and documentation."
    }
]

# Module names for services that this entity/module can perform.
class ServiceModules(Enum):
    Build3DStructure = build3DStructure 
    Evaluate = evaluate
    Status = get_status
    Validate = validate
    Default = get_status

Operation_Order = [
    'Status',
    'Validate',
    'Evaluate',
    'Build3DStructure'
]


class subEntities(GemsStrEnum) :
    Graph = 'graph'

class AvailableServices(GemsStrEnum):
    build3dStructure = 'Build3DStructure'
    drawGlycan = 'DrawGlycan'
    evaluate = 'Evaluate'
    status = 'Status'


class Environment(GemsStrEnum):
    # The entity itself
    sequenceentity = 'GEMS_MODULES_SEQUENCE_PATH'
    # Services for this entity, in alphabetical order
    build3DStructure = 'GEMS_MODULES_SEQUENCE_STRUCTURE_PATH'
    graph = 'GEMS_MODULES_SEQUENCE_GRAPH_PATH'
    evaluate = 'GEMS_MODULES_SEQUENCE_STRUCTURE_PATH'

# ## Recognized input and output formats
# ##


class Formats(GemsStrEnum):
    """All Sequenes must be in GLYCAM Condensed notation"""
    # the basic sequence as it might arrive, unspecified order, assumed condensed glycam
    sequence = 'Sequence'


class Locations(GemsStrEnum):
    # < All input at this time must be internal to the JSON object(s)
    internal = 'internal'
