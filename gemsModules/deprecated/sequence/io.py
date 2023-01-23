#!/usr/bin/env python3
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union, Any
from typing import ForwardRef
from os.path import join
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError, validator
from pydantic.schema import schema
from gemsModules.deprecated.common.loggingConfig import loggers, createLogger
from gemsModules.deprecated.common import io as commonio
from gemsModules.deprecated.project import io as projectio
from gemsModules.deprecated.project import projectUtilPydantic as projectUtils
from gemsModules.deprecated.sequence import settings
from gemsModules.deprecated.sequence import evaluate
from gemsModules.deprecated import sequence
import traceback


if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


class Resource(commonio.Resource):
    locationType: settings.Locations = Field(
        'internal',
        description='Supported input locations for the Service Entity.'
    )
    resourceFormat: settings.Formats = Field(
        'GlycamCondensed',
        description='Supported input formats for the Service Entity.'
    )


class TheSequence(BaseModel):
    payload: str = ''
    sequenceFormat: str = Field(
        'GlycamCondensed',
        alias='format',
        description='The format of the sequence in the payload'
    )

    class Config:
        title = 'Sequence'


class TheSequenceVariants(BaseModel):
    """Different representations of the sequence."""
    # condensed sequence types
    indexOrdered: str = None  # key is 'indexOrdered' ???
    longestChainOrdered: str = None
    userOrdered: str = None
    monospacedTextDiagram: str = None
    # ... labeled
    indexOrderedLabeled: str = None
    longestChainOrderedLabeled: str = None
    userOrderedLabeled: str = None
    monospacedTextDiagramLabeled: str = None
    # other condensed sequence representations
    suuid: str = None
    smd5sum: str = None

    # ## I'm certain there is a better way to do this.  - Lachele
    def getSequenceVariant(self, variant):
        log.info("TheSequenceVariants.getSequenceVariant was called")
        theVariant = getattr(self, variant)
        return theVariant


class Definitions(BaseModel):
    """TODO:  write this. """
    pass


class TheSystemSolvationOptions(BaseModel):
    solvationStatus: str = Field(
        'Unsolvated',
        description="Unsolvated, To be solvated, Solvated, Not applicable"
    )
    ionStatus: str = Field(
        'No ions',
        description="No ions, Add ions, Contains ions."
    )


class TheResidueRingPucker(BaseModel):
    puckerClassificationSystem: str = Field(
        'BFMP',
        description="The system used to identify the ring pucker (shape)."
    )


class TheRotamerDihedralInfo(BaseModel):
    dihedralName: str = None  # phi, psi etc.
    dihedralValues: List[str] = []  # gg, -g, tg, etc


class SingleLinkageRotamerData(BaseModel):
    indexOrderedLabel: str = None
    linkageLabel: str = None
    linkageName: str = None
    firstResidueNumber: str = None
    secondResidueNumber: str = None
    dihedralsWithOptions: List[str] = []
    possibleRotamers: List[TheRotamerDihedralInfo] = []
    likelyRotamers: List[TheRotamerDihedralInfo] = []
    selectedRotamers: List[TheRotamerDihedralInfo] = []


class TheResidueGeometryOptions(BaseModel):
    """Geometry options for residues"""
    ringPuckers: List[TheResidueRingPucker] = []


class AllLinkageRotamerInfo(BaseModel):
    """Geometry options for linkages"""
    singleLinkageRotamerDataList: List[SingleLinkageRotamerData] = []
    totalLikelyRotamers: int = 0
    totalPossibleRotamers: int = 0
    totalSelectedRotamers: int = 0

    def __init__(self, **data: Any):
        super().__init__(**data)

        if self.singleLinkageRotamerDataList != []:
            from gemsModules.deprecated.sequence import structureInfo
            if self.totalSelectedRotamers == 0:
                self.totalSelectedRotamers = structureInfo.countNumberOfShapes(
                    self, 'Selected')
            if self.totalPossibleRotamers == 0:
                self.totalPossibleRotamers = structureInfo.countNumberOfShapes(
                    self, 'Possible')
            if self.totalLikelyRotamers == 0:
                self.totalLikelyRotamers = structureInfo.countNumberOfShapes(
                    self, 'Likely')

# @class Single3DStructureBuildDetails
#    @brief An object that represents one requested build state and its outputs
#    @TODO: Add more fields, ringPucker, protonationState, etc...


class Single3DStructureBuildDetails(BaseModel):
    ##################################
    # This class was built by merging two older classes.  Therefore, some names
    # might appear to be duplicates.  They might even be duplicates.  There
    # is no time now for this sort of cleaning now.  Please feel free to do so.
    ##################################
    # The timestamp associated with the information generated by this class.
    date: datetime = None
    # The status of the build:
    #     new, building, ready, submitted, complete, failed, delayed
    status: str = "new"
    # payload, here, is the projectID, useful for finding output
    payload: str = ""
    # For convenience:
    # The sequence that inspired this build is contained here.
    # This should be the official version that is used to generate the primary
    # key for database searches.  See seqID.
    pUUID: str = ""
    entity_id: str = ""
    service_id: str = ""
    incomingSequence: str = ""
    indexOrderedSequence: str = ""
    # For convenience:
    # The seqID is a UUID hash of the sequence.  The seqID is used as a primary
    # key for retrieving information about the sequence from databases.
    seqID: str = ""
    # conformerID contains a terse label representing the structural details
    #    of this conformer.  It might encode rotamer names, ring pucker,
    #    protonation state, etc.  If there is only one conformational isomer
    #    available for this structure, it is simply 'structure'.
    conformerID: str = ""
    # conformerLabel may be either :
    #    * the same as the conformerID
    #    * a uuid made from the conformer ID if the conformerID is  > 32 char long.
    #  The conformerLabel is used to name directories and files.  The 32 character
    #  limit keeps directories from becoming difficult to read.  it also helps keep
    #  file names and paths from exceeding length limits.
    conformerLabel: str = ""
    #  The sequenceConformation is a more human-readable description of the
    #  structural details of the conformer.  It contains the same information as
    #  the conformerID.
    #  This structure has been considered, but it might not give us the needed
    #  flexibility:  sequenceConformation : List[RotamerConformation] = None
    #  Oliver says this:
    #      Would be nice to just directly use the gmml level class like this:
    #      gmmlConformerInfo : gmml.single_rotamer_info_vector = None
    sequenceConformation: List = []
    #  When there are multiple structures, one is chosen for the default.
    isDefaultStructure: bool = False
    isNewBuild: bool = False
    # The following are locations needed by builders and/or retrievers.
    structureDirectoryName: str = ""
    filesystem_path: str = ""
    host_url_base_path: str = ""
    conformer_path: str = ""
    absolute_conformer_path: str = ""
    downloadUrlPath: str = ""
    # The following are options relevant to how the structure is built.
#    simulationPhase : str = "gas-phase"  ## also solvent model, e.g., TIP3P, TIP5P
#    solvationShape : str = None   ## Solvated requests might specify a shape.
#    addIons : str = "default" ## Is there a benefit for this to be a String? Boolean?
#    energy : str = None ## kcal/mol
    # TODO: This needs to be a class. Schedule design with Lachele.
    forceField: str = 'See Build Directory Files'

    def __init__(self, **data: Any):
        super().__init__(**data)

        log.debug(
            "These are the values at initialization of Single3DStructureBuildDetails")
        log.debug("payload(projectID): " + self.payload)
        log.debug("incomingSequence: " + self.incomingSequence)
        log.debug("indexOrderedSequence: " + self.indexOrderedSequence)
        log.debug("seqID: " + self.seqID)
        log.debug("conformerID: " + self.conformerID)
        log.debug("conformerLabel: " + self.conformerLabel)
        log.debug("conformerPath: " + self.conformer_path)
        log.debug("downloadUrlPath: " + self.downloadUrlPath)

    # Plain setters because logic elsewhere should determine them

    def setIsNewBuild(self, IsNewBuild: bool):
        self.isNewBuild = IsNewBuild

    def setEntityId(self, theEntityId: str):
        self.entity_id = theEntityId

    def setServiceId(self, theServiceId: str):
        self.service_id = theServiceId

    def setPuuid(self, thePuuid: str):
        self.pUUID = thePuuid

    def setFilesystemPath(self, thePath: str):
        self.filesystem_path = thePath

    def setHostUrlBasePath(self, thePath: str):
        self.host_url_base_path = thePath

    def setConformerLabel(self, theLabel: str):
        self.conformerLabel = theLabel

    def setConformerId(self, theId: str):
        self.conformerID = theId

    def setStructureDirectoryName(self, theStructureDirectoryName: str):
        self.structureDirectoryName = theStructureDirectoryName

    def setIndexOrderedSequence(self, theIndexOrderedSequence: str):
        self.indexOrderedSequence = theIndexOrderedSequence

    def setDownloadUrlPath(self, theDownloadUrlPath: str):
        self.downloadUrlPath = theDownloadUrlPath

    # Setters that contain logic

    # theBuildDir is usually "New_Builds" or "Existing_Builds" unlesss it is the general case
    def setAbsoluteConformerPath(self, theBuildDir: str):
        self.absolute_conformer_path = join(
            self.filesystem_path,
            self.entity_id,
            self.service_id,
            'Builds',
            self.pUUID,
            theBuildDir,
            self.structureDirectoryName)

    def setConformerPath(self):
        self.conformer_path = join(
            self.filesystem_path,
            self.entity_id,
            self.service_id,
            'Builds',
            self.pUUID,
            'Requested_Builds',
            self.structureDirectoryName)

    def setSeqId(self, theSeqID: str = None):  # does this need a noclobber option?
        if theSeqID is not None:
            self.seqID = theSeqID
            return
        if self.indexOrderedSequence == "":
            error = "Cannot derive a seqID from an empty indexOrderedSequence string"
            log.error(error)
            raise error
        self.seqID = projectUtils.getSeqIdForSequence(
            self.indexOrderedSequence)

    # All the getters are plain so far

    def getEntityId(self):
        return self.entity_id

    def getServiceId(self):
        return self.service_id

    def getConformerPath(self):
        return self.conformer_path

    def getAbsoluteConformerPath(self):
        return self.absolute_conformer_path

    def getDownloadUrlPath(self):
        return self.downloadUrlPath

    def getSeqId(self):
        return self.seqID

    def getFilesystemPath(self):
        return self.filesystem_path

    def getHostUrlBasePath(self):
        return self.host_url_base_path

    def getConformerLabel(self):
        return self.conformerLabel

    def getConformerID(self):
        return self.conformerID

    def getStructureDirectoryName(self):
        return self.structureDirectoryName

    def getIndexOrderedSequence(self):
        return self.indexOrderedSequence

# @class StructureBuildInfo
#    @brief An object to represent the data previously held in the Structure_Mapping_Table.
#    @detail This object holds the data that describes a series of ways that this single structure
#            has been built. Each variation of a rotamer or from gas-phase to solvated, etc...
#            represents a different build state, and each gets a record in this object.
#            This object can be used to track a request, and a copy of it could be used to track
#            the progress of that requested series of jobs.


class StructureBuildInfo(BaseModel):
    # Useful to know what this all applies to.
    incomingSequence: str = ""
    indexOrderedSequence: str = ""
    seqID: str = ""  # UUID based on indexOrderedSequence
    # A build state is a descriptive object that can be used to request a pdb file
    #    of a sequence in a specific pose, with various other settings as well.
    individualBuildDetails: List[Single3DStructureBuildDetails] = []
    buildStrategyID: str = 'buildStrategyID1'

    def setIncomingSequence(self, inputSequence):
        self.incomingSequence = inputSequence

    def setIndexOrderedSequence(self, inputSequence):
        self.indexOrderedSequence = inputSequence

    def setBuildStrategyID(self, newBuildStrategyID):
        self.buildStrategyID = newBuildStrategyID

    def setSeqId(self):
        if self.indexOrderedSequence == "":
            error = "Cannot derive a seqID from an empty indexOrderedSequence string"
            log.error(error)
            raise error
        self.seqID = projectUtils.getSeqIdForSequence(
            self.indexOrderedSequence)

    def getIndividualBuildDetails(self):
        return self.individualBuildDetails

    def getBuildStrategyID(self):
        return self.buildStrategyID

    def getSequence(self):
        return self.sequence

    def getSeqId(self):
        return self.seqID


class TheLinkageGeometryOptions(BaseModel):
    linkageRotamerInfo: AllLinkageRotamerInfo = None

    def getRotamerData(self):
        log.info("Linkage GeometryOptions.getRotamerData was called")
        if self.linkageRotamerInfo is None:
            return None
        else:
            return self.linkageRotamerInfo

    def createRotamerData(self):
        log.info("Linkage geometry options.createRotamerDataOut was called")
        if self.linkageRotamerInfo is None:
            self.linkageRotamerInfo = AllLinkageRotamerInfo()
        self.linkageRotamerInfo.createRotamerData()

    def setLinkageRotamerInfo(self, validatedSequence: str):
        from gemsModules.deprecated.sequence import evaluate
        self.linkageRotamerInfo = evaluate.getLinkageOptionsFromGmmlcbBuilder(
            validatedSequence)
        log.debug(self.linkageRotamerInfo.json())

# I can't figure out if I can pass gmml classes to functions here, so I just
# wrote getLinkageOptionsFromGmmlcbBuilder.


class TheGeometryOptions(BaseModel):
    residues: TheResidueGeometryOptions = None  # Not yet handled.
    linkages: TheLinkageGeometryOptions = None

    def __init__(self, **data: Any):
        super().__init__(**data)

    def getRotamerData(self):
        log.info("GeometryOptions.getRotamerData was called")
        if self.linkages is None:
            return None
        elif self.linkages.linkageRotamerInfo is None:
            return None
        else:
            return self.linkages.linkageRotamerInfo

    def createRotamerData(self):
        log.info("Geometry options.createRotamerDataOut was called")
        if self.linkages is None:
            self.linkages = TheLinkageGeometryOptions()
        if self.linkages.linkageRotamerInfo is None:
            self.linkages.linkageRotamerInfo = AllLinkageRotamerInfo()
        self.linkages.linkageRotamerInfo.createRotamerData()

    def setLinkageRotamerInfo(self, validatedSequence: str):
        if self.linkages is None:
            self.linkages = TheLinkageGeometryOptions()
        self.linkages.setLinkageRotamerInfo(validatedSequence)
#        from gemsModules.deprecated.sequence import evaluate
#        self.linkages = evaluate.getLinkageOptionsFromGmmlcbBuilder(validatedSequence)
#        log.debug(self.linkages.json())


class TheBuildOptions(BaseModel):
    """Options for building 3D models"""
    # Generated by evaluation.  Used in builds.
    solvationOptions: TheSystemSolvationOptions = None  # Not yet handled.
    geometryOptions: TheGeometryOptions = None
    mdMinimize: bool = Field(
        True,
        title='Minimize structure using MD',
    )
    numberStructuresHardLimit: int = None  # Website or API calls will enforce 64
    # Set to -1 to get all of them (BEWARE!)

    def __init__(self, **data: Any):
        super().__init__(**data)

    def setGeometryOptions(self, validatedSequence: str):
        log.info("Setting geometryOptions in BuildOptions")
        log.debug("validatedSequence: " + validatedSequence)
        self.geometryOptions = TheGeometryOptions()
        self.geometryOptions.setLinkageRotamerInfo(validatedSequence)

    def getRotamerData(self):
        log.info("buildOptions.getRotamerDataOut was called")
        if self.geometryOptions is None:
            return None
        else:
            return self.geometryOptions.getRotamerData()

    def createRotamerData(self):
        log.info("Build Options.createRotamerDataOut was called")
        if self.geometryOptions is None:
            self.geometryOptions = TheGeometryOptions()
        self.geometryOptions.createRotamerData()


class TheDrawOptions(BaseModel):
    """Options for drawing 2D models"""
    Labeled: bool = True


class TheEvaluationOptions(BaseModel):
    """Options for sequence evaluations"""
    validateOnly: bool = False  # Stop after setting sequenceIsValid and return answer
    # Is this an evaluation as part of an explicit build request?
    evaluateForBuild: bool = False
    noBuild: bool = False  # Just do a full evaluation ; don't do the default example build


class TheSequenceEvaluationOutput(BaseModel):
    # Determine if the sequence has proper syntax, etc.
    sequenceIsValid: bool = False
    sequenceVariants: TheSequenceVariants = None
    evaluationOptions: TheEvaluationOptions = Field(
        None,
        description="Options for evaluating the sequence."
    )
    buildOptions: TheBuildOptions = Field(
        None,
        description="Options for building the 3D Structure of the sequence."
    )
    drawOptions: TheDrawOptions = Field(
        None,
        description="Options for drawing a 2D Structure of the sequence."
    )

    def __init__(self, **data: Any):
        super().__init__(**data)

    def getRotamerData(self):
        log.info("sequenceEvaluationOutput.getRotamerData was called")
        if self.buildOptions is None:
            return None
        else:
            return self.buildOptions.getRotamerData()

    def createRotamerData(self):
        log.info("Sequence evaluation data.createRotamerDataOut was called")
        if self.buildOptions is None:
            self.buildOptions = TheBuildOptions()
        self.buildOptions.createRotamerData()

    def getEvaluation(self, sequence: str, validateOnly):
        log.info("Getting the Evaluation for SequenceEvaluationOutput.")

        log.debug("sequence: " + repr(sequence))
        log.debug("validateOnly: " + repr(validateOnly))

        from gemsModules.deprecated.sequence import evaluate

        if self.evaluationOptions is None:
            self.evaluationOptions = TheEvaluationOptions()

        self.evaluationOptions.validateOnly = validateOnly
        #self.sequenceIsValid = evaluate.checkIsSequenceSane(sequence)
        self.sequenceIsValid = True; # If we got to here, it's already been checked.
        log.debug("self.sequenceIsValid: " + str(self.sequenceIsValid))

        if self.sequenceIsValid:
            self.sequenceVariants = TheSequenceVariants()
            self.sequenceVariants = evaluate.getSequenceVariants(sequence)
            log.debug("Just got sequence variants.  They are:")
            log.debug(str(self.sequenceVariants))
###
# I think these are no longer needed.
###
            #log.debug("indexOrdered: " + str(self.sequenceVariants['indexOrdered']))
            #reducingSuffix = self.sequenceVariants['indexOrdered'][-7:]
            log.debug("indexOrdered: " +
                      str(self.sequenceVariants.indexOrdered))
            reducingSuffix = self.sequenceVariants.indexOrdered[-7:]
            log.debug("reducingSuffix: " + reducingSuffix)
            log.debug("# of '-': " + str(reducingSuffix.count('-')))
#            if 2 == reducingSuffix.count('-'):
#                lastIndex = self.sequenceVariants['indexOrdered'].rfind('-')
#                log.debug("lastIndex of '-': " + str(lastIndex))
#                self.sequenceVariants['indexOrdered'] = self.sequenceVariants['indexOrdered'][:lastIndex - 2] + self.sequenceVariants['indexOrdered'][lastIndex:]
#                log.debug("indexOrdered: " + self.sequenceVariants['indexOrdered'])
            # DGlcpNAcb1-1-OH

        if self.sequenceIsValid and not self.evaluationOptions.validateOnly:
            self.buildOptions = TheBuildOptions()
            self.buildOptions.setGeometryOptions(sequence)

       # self.defaultStructure
        # drawOptions to be developed later.

    # ## I'm certain there is a better way to do this.  - Lachele
    def getSequenceVariant(self, variant):
        log.debug("TheSequenceEvaluationOutput.getSequenceVariant was called")
        # if not 'Evaluate' in  self.responses.Keys() :
        if self.sequenceVariants is None:
            return None
        else:
            theVariant = getattr(self.sequenceVariants, variant)
            return theVariant


# ## These do not need to be named with 'sequence, e.g., 'sequenceService'.
# ## Doing that just makes me feel more comfortable about referencing things.
# ##
# ## Regarding capitalization, my current ad-hoc convention:
# ##    - initial is lower case = this is a child class of something else and
# ##      the first word is the modifier.
# ##          example:  sequenceService is a child of Service, modified by sequence
# ##    - initial is upper case = this is not a child, except of BaseModel.
# ##          example:  SequenceInputs is not a child of another class
# ## Feel free to change the naming conventions
# ## (Lachele)
class sequenceService(commonio.Service):
    """Holds information about a Service requested of the Sequence Entity."""
    typename: settings.Services = Field(
        'Evaluate',
        alias='type',
        title='Requested Service',
        description='The service requested of the Sequence Entity'
    )

    def __init__(self, **data: Any):
        super().__init__(**data)
        log.info("Initializing Service.")
        log.debug("the data " + repr(self))
        log.debug("Init for the Services in sequence was called.")


# This is a Response and should be called that
class SequenceOutputs(BaseModel):
    sequenceEvaluationOutput: TheSequenceEvaluationOutput = None
    structureBuildInfo: StructureBuildInfo = None

    def getStructureBuildInfo(self):
        if self.structureBuildInfo is None:
            return None
        else:
            return self.structureBuildInfo

    def getBuildStrategyID(self):
        if self.structureBuildInfo is None:
            return None
        else:
            return self.structureBuildInfo.getBuildStrategyID()

    def getSequence(self):
        if self.structureBuildDetails is None:
            return None
        else:
            return self.structureBuildInfo.getSequence()

    def getRotamerData(self):
        log.info("evaluate.getRotamerData was called")
        if self.sequenceEvaluationOutput is None:
            return None
        else:
            return self.sequenceEvaluationOutput.getRotamerData()

    def createRotamerData(self):
        log.info("Sequence outputs.createRotamerDataOut was called")
        if self.sequenceEvaluationOutput is None:
            self.sequenceEvaluationOutput = TheSequenceEvaluationOutput()
        self.sequenceEvaluationOutput.createRotamerData()


class SequenceInputs(BaseModel):
    sequence: TheSequence = None
    sequenceVariants: TheSequenceVariants = None
    systemSolvationOptions: TheSystemSolvationOptions = None
    geometryOptions: TheGeometryOptions = None
    buildOptions: TheBuildOptions = None
    evaluationOptions: TheEvaluationOptions = None
    drawOptions: TheDrawOptions = None


class sequenceEntity(commonio.Entity):
    """Holds information about the main object responsible for a service."""
    entityType: str = Field(
        settings.WhoIAm,
        title='Type',
        alias='type'
    )
    services: Dict[str, sequenceService] = {}
    inputs: SequenceInputs = None
    outputs: SequenceOutputs = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        log.info("Instantiating a sequenceEntity")
        log.debug("entityType: " + self.entityType)

    # ## I'm certain there is a better way to do this.  - Lachele
    def getInputSequencePayload(self):
        log.info("sequenceEntity.getInputSequencePayload was called")
        if self.inputs is None:
            return None
        elif self.inputs.sequence is None:
            return None
        elif self.inputs.sequence.payload is None:
            return None
        else:
            return self.inputs.sequence.payload

    def getBuildStrategyIDOut(self):
        if self.outputs is None:
            return None
        else:
            return self.outputs.getBuildStrategyID()

    def getBuildSequenceOut(self):
        if self.outputs is None:
            return None
        else:
            return self.outputs.getSequence()

    def getRotamerDataIn(self):
        log.info("Entity.getRotamerDataIn was called")
        if self.inputs is None:
            log.debug("inputs is None. returning None.")
            return None
        elif self.inputs.geometryOptions is None:
            log.debug("inputs.geometryOptions is None. returning None.")
            return None
        else:
            return self.inputs.geometryOptions.getRotamerData()

    def getRotamerDataOut(self):
        log.info("Entity.getRotamerDataOut was called")
        if self.outputs is None:
            return None
        else:
            return self.outputs.getRotamerData()

    def createRotamerDataOut(self):
        log.info("Entity.createRotamerDataOut was called")
        if self.outputs is None:
            self.outputs = SequenceOutputs()
        self.outputs.createRotamerData()

    # ## I'm certain there is a better way to do this.  - Lachele
    def getSequenceVariantIn(self, variant):
        log.info("sequenceEntity.getSequenceVariantIn was called")
        if self.inputs is None:
            return None
        elif self.inputs.sequenceVariants is None:
            return None
        else:
            return self.inputs.sequenceVariants[variant]

    # ## I'm certain there is a better way to do this.  - Lachele
    def getSequenceVariantOut(self, variant):
        log.debug("sequenceEntity.getSequenceVariantOut was called")
        if self.outputs is None:
            log.debug("sequenceEntity.getSequenceVariantOut found NO OUPUTS")
            return None
        elif self.outputs.sequenceEvaluationOutput is None:
            log.debug(
                "sequenceEntity.getSequenceVariantOut found NO Sequence Evaluation Output")
            return None
        else:
            log.debug(
                "sequenceEntity.getSequenceVariantOut attempting to return variant.")
            return self.outputs.sequenceEvaluationOutput.getSequenceVariant(variant)

    def validateCondensedSequence(self, validateOnly: bool = False):
        self.evaluateCondensedSequence(validateOnly=True)

    def evaluateCondensedSequence(self, validateOnly: bool = False):
        if self.inputs is None:
            thisAdditionalInfo = {'hint', 'The entity has no defined inputs.'}
            self.generateCommonParserNotice(
                noticeBrief='EmptyPayload',
                scope='SequenceEntity',
                additionalInfo=thisAdditionalInfo
            )
            raise
        if self.inputs.sequence is None:
            thisAdditionalInfo = {
                'hint': 'The entity has inputs but cannot find Sequence Payload.'}
            self.generateCommonParserNotice(
                noticeBrief='EmptyPayload',
                scope='SequenceEntityInputs',
                additionalInfo=thisAdditionalInfo
            )
            raise
        sequence = self.inputs.sequence.payload
        if sequence is None or "":
            thisAdditionalInfo = {
                'hint': 'The entity a Sequence but cannot find Sequence Payload.'}
            self.generateCommonParserNotice(
                noticeBrief='EmptyPayload',
                scope='SequenceEntityInputSequence',
                additionalInfo=thisAdditionalInfo
            )
            raise
        if self.outputs is None:
            self.outputs = SequenceOutputs()
        if self.outputs.sequenceEvaluationOutput is None:
            self.outputs.sequenceEvaluationOutput = TheSequenceEvaluationOutput()
        self.outputs.sequenceEvaluationOutput.getEvaluation(
            sequence, validateOnly)


class sequenceTransactionSchema(commonio.TransactionSchema):
    """
    Holds info about the Transaction JSON object used in the Sequence entity.
    """
    # ... means a value is required in Pydantic.
    entity: sequenceEntity = ...
    project: projectio.CbProject = None

    def __init__(self, **data: Any):
        super().__init__(**data)

    class Config:
        title = 'gensModulesSequenceTransaction'

    # ## I'm certain there is a better way to do this.  - Lachele
    def getInputSequencePayload(self):
        log.info("sequenceTransactionSchema.getInputSequencePayload was called")
        if self.entity is None:
            return None
        else:
            return self.entity.getInputSequencePayload()

    def getRotamerDataIn(self):
        log.info("Transaction.getRotamerDataIn was called")
        if self.entity is None:
            return None
        else:
            return self.entity.getRotamerDataIn()

    def getRotamerDataOut(self):
        log.info("Transaction.getRotamerDataOut was called")
        if self.entity is None:
            return None
        else:
            return self.entity.getRotamerDataOut()

    def createRotamerDataOut(self):
        log.info("Transaction.createRotamerDataOut was called")
        if self.entity is None:
            self.entity = sequenceEntity()
        self.entity.createRotamerDataOut()

    def getBuildStrategyIDOut(self):
        if self.entity is None:
            return None
        else:
            return self.entity.getBuildStrategyIDOut()

    def getBuildSequenceOut(self):
        if self.entity is None:
            return None
        else:
            return self.entity.getSequence()

    # ## I'm certain there is a better way to do this.  - Lachele
    def getSequenceVariantIn(self, variant):
        log.info("sequenceTransactionSchema.getSequenceVariantIn was called")
        if self.entity is None:
            return None
        else:
            return self.entity.getSequenceVariantIn(variant)

    # ## I'm certain there is a better way to do this.  - Lachele
    def getSequenceVariantOut(self, variant):
        log.info("sequenceTransactionSchema.getSequenceVariantOut was called")
        if self.entity is None:
            return None
        else:
            return self.entity.getSequenceVariantOut(variant)

    def evaluateCondensedSequence(self):
        if self.entity is None:
            thisAdditionalInfo = {
                'hint': 'The transaction has no defined entity.'}
            self.generateCommonParserNotice(
                noticeBrief='GemsError',
                scope='SequenceTransaction',
                additionalInfo=thisAdditionalInfo
            )
            raise error
        self.entity.evaluateCondensedSequence()


class Transaction(commonio.Transaction):
    transaction_in: sequenceTransactionSchema
    transaction_out: sequenceTransactionSchema

    def populate_transaction_in(self):
        log.info("sequence - Transaction.populate_transaction_in was called")
        self.transaction_in = sequenceTransactionSchema(**self.request_dict)
        log.debug("The transaction_in is: ")
        log.debug(self.transaction_in.json(indent=2))

    def initialize_transaction_out_from_transaction_in(self):
        log.info("initialize_transaction_out_from_transaction_in was called")
        self.transaction_out = self.transaction_in.copy(deep=True)
        log.debug("The transaction_out is: ")
        log.debug(self.transaction_out.json(indent=2))

    def doDefaultService():
        from gemsModules.deprecated.receive import doDefaultService
        doDefaultService(self)
        return self

    def getRotamerDataIn(self):
        log.info("Transaction-Wrapper.getRotamerDataIn was called")
        if self.transaction_in is None:
            return None
        else:
            return self.transaction_in.getRotamerDataIn()

    def getRotamerDataOut(self):
        log.info("Transaction-Wrapper.getRotamerDataOut was called")
        if self.transaction_out is None:
            return None
        else:
            return self.transaction_out.getRotamerDataOut()

    def createRotamerDataOut(self):
        log.info("Transaction-Wrapper.createRotamerDataOut was called")
        if self.transaction_out is None:
            self.transaction_out = sequenceTransactionSchema()
        return self.transaction_out.createRotamerDataOut()

    # ## I'm certain there is a better way to do this.  - Lachele
    def getInputSequencePayload(self):
        log.info("sequence - Transaction.getInputSequencePayload was called")
        if self.transaction_in is None:
            return None
        else:
            return self.transaction_in.getInputSequencePayload()

    # These project-based ones should really depend more on project
    def getPuuIDOut(self):
        if self.transaction_out is None:
            return None
        if self.transaction_out.project is None:
            return None
        if self.transaction_out.project.pUUID is None:
            return None
        else:
            return self.transaction_out.project.pUUID

    def getProjectDirOut(self):
        if self.transaction_out is None:
            return None
        if self.transaction_out.project is None:
            return None
        if self.transaction_out.project.project_dir is None:
            return None
        else:
            return self.transaction_out.project.project_dir

    def getIsEvaluationSetNoBuild(self):
        if all(v is not None for v in [
            self.transaction_out,
            self.transaction_out.entity,
            self.transaction_out.entity.outputs,
            self.transaction_out.entity.outputs.sequenceEvaluationOutput,
            self.transaction_out.entity.outputs.sequenceEvaluationOutput.evaluationOptions
        ]):
            return self.transaction_out.entity.outputs.evaluationOptions.noBuild
        else:
            return False  # the default value if not set otherwise

    def setIsEvaluationSetNoBuild(self, value):
        if all(v is not None for v in [
            self.transaction_out,
            self.transaction_out.entity,
            self.transaction_out.entity.outputs,
            self.transaction_out.entity.outputs.sequenceEvaluationOutput,
            self.transaction_out.entity.outputs.sequenceEvaluationOutput.evaluationOptions
        ]):
            self.transaction_out.entity.outputs.evaluationOptions.noBuild = value
        else:
            self.generateCommonParserNotice(
                noticeBrief='GemsError',
                additionalInfo={"hint": "cannot set noBuild option"})

    def getIsEvaluationForBuild(self):
        if all(v is not None for v in [
            self.transaction_out,
            self.transaction_out.entity,
            self.transaction_out.entity.outputs,
            self.transaction_out.entity.outputs.sequenceEvaluationOutput,
            self.transaction_out.entity.outputs.sequenceEvaluationOutput.evaluationOptions
        ]):
            return self.transaction_out.entity.outputs.sequenceEvaluationOutput.evaluationOptions.evaluateForBuild
        else:
            return False  # the default value if not set otherwise

    def setIsEvaluationForBuild(self, value):
        if all(v is not None for v in [
            self.transaction_out,
            self.transaction_out.entity,
            self.transaction_out.entity.outputs,
            self.transaction_out.entity.outputs.sequenceEvaluationOutput,
            self.transaction_out.entity.outputs.sequenceEvaluationOutput.evaluationOptions
        ]):
            self.transaction_out.entity.outputs.sequenceEvaluationOutput.evaluationOptions.evaluateForBuild = value
        else:
            self.generateCommonParserNotice(
                noticeBrief='GemsError',
                additionalInfo={"hint": "cannot set evaluateForBuild option"})

    def getNumberStructuresHardLimitIn(self):
        if all(v is not None for v in [
            self.transaction_in,
            self.transaction_in.entity,
            self.transaction_in.entity.inputs,
            self.transaction_in.entity.inputs.buildOptions
        ]):
            return self.transaction_in.entity.inputs.buildOptions.numberStructuresHardLimit
        else:
            return None

    def setNumberStructuresHardLimitOut(self, value):
        if all(v is not None for v in [
            self.transaction_out,
            self.transaction_out.entity,
            self.transaction_out.entity.outputs,
            self.transaction_out.entity.outputs.sequenceEvaluationOutput,
            self.transaction_out.entity.outputs.sequenceEvaluationOutput.buildOptions
        ]):
            self.transaction_out.entity.outputs.sequenceEvaluationOutput.buildOptions.numberStructuresHardLimit = value
        else:
            self.generateCommonParserNotice(
                noticeBrief='GemsError',
                additionalInfo={"hint": "cannot set limit for number of structures"})
            return None
    # TODO - write all these if-not-None-return recursions to look like the ones above.

    def getSeqIdOut(self):
        if self.transaction_out is None:
            return None
        if self.transaction_out.entity is None:
            return None
        if self.transaction_out.entity.outputs is None:
            return None
        if self.transaction_out.entity.outputs.structureBuildInfo is None:
            return None
        if self.transaction_out.entity.outputs.structureBuildInfo.seqID is None:
            return None
        else:
            return self.transaction_out.entity.outputs.structureBuildInfo.seqID

    def getStructureBuildInfoOut(self):
        if self.transaction_out is None:
            return None
        if self.transaction_out.entity is None:
            return None
        if self.transaction_out.entity.outputs is None:
            return None
        if self.transaction_out.entity.outputs.structureBuildInfo is None:
            return None
        else:
            return self.transaction_out.entity.outputs.structureBuildInfo

    def getIndividualBuildDetailsOut(self):
        if self.transaction_out is None:
            return None
        if self.transaction_out.entity is None:
            return None
        if self.transaction_out.entity.outputs is None:
            return None
        if self.transaction_out.entity.outputs.structureBuildInfo is None:
            return None
        if self.transaction_out.entity.outputs.structureBuildInfo.individualBuildDetails is None:
            return None
        if self.transaction_out.entity.outputs.structureBuildInfo.individualBuildDetails == []:
            return None
        else:
            return self.transaction_out.entity.outputs.structureBuildInfo.individualBuildDetails

    def getBuildStrategyIDOut(self):
        if self.transaction_out is None:
            return None
        else:
            return self.transaction_out.getBuildStrategyIDOut()

    def getBuildSequenceOut(self):
        if self.transaction_out is None:
            return None
        else:
            return self.transaction_out.getSequence()

    # ## I'm certain there is a better way to do this.  - Lachele
    def getSequenceVariantIn(self, variant):
        log.info("sequence - Transaction.getSequenceVariantIn was called")
        if self.transaction_in is None:
            return None
        else:
            return self.transaction_in.getSequenceVariantIn(variant)

    # ## I'm certain there is a better way to do this.  - Lachele
    def getSequenceVariantOut(self, variant):
        log.info("sequence - Transaction.getSequenceVariantOut was called")
        if self.transaction_out is None:
            return None
        else:
            return self.transaction_out.getSequenceVariantOut(variant)

    def evaluateCondensedSequence(self):
        if self.transaction_out is None and self.transaction_in is None:
            thisAdditionalInfo = {
                'hint': 'Neither the transaction_in nor the transaction_out are populated.'}
            self.generateCommonParserNotice(
                noticeBrief='NoInputPayloadDefined',
                scope='TransactionWrapper.EvaluateCondensedSequence',
                additionalInfo=thisAdditionalInfo
            )
            raise error
        if self.transaction_out is None:
            self.initialize_transaction_out_from_transaction_in()
        self.transaction_out.evaluateCondensedSequence()

# In file _manageSequenceBuild3DStructureRequest.py:
#    def manageSequenceBuild3DStructureRequest(self, defaultOnly : bool = False)
    from gemsModules.deprecated.sequence._manageSequenceBuild3DStructureRequest import manageSequenceBuild3DStructureRequest

    def build_outgoing_string(self):
        if self.transaction_out.prettyPrint is True:
            self.outgoing_string = self.transaction_out.json(indent=2)
        else:
            self.outgoing_string = self.transaction_out.json()


def generateSchema():
    import json
 #   print(Entity.schema_json(indent=2))
    print(sequenceTransactionSchema.schema_json(indent=2))


inputJSON = '{ "entity": { "type": "Sequence", "services":  { "Build": { "type": "Build3DStructure" } } , "inputs":  { "Sequence": { "payload": "DManpa1-OH" } } } }'


def troubleshoot():
    thisTransaction = Transaction(inputJSON)
    print(thisTransaction.incoming_string)
    print(thisTransaction.request_dict)
    thisTransaction.populate_transaction_in()
    print(thisTransaction.transaction_in)


if __name__ == "__main__":
    generateSchema()
    troubleshoot()
