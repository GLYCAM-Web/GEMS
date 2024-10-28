#!/usr/bin/env bash

EvaluationTests=(
	ListRSeqsSeqID
	DefaultSymlink
	EvalJsonOutput
	MinGasPdb
)

PDB_File_To_Test="${sequenceBuildsPath}/${evaluation_pUUID}/New_Builds/${defaultStructureConformationID}/min-gas.pdb"

declare -A EvaluationCommands
EvaluationCommands=(
	[ListRSeqsSeqID]="/bin/ls -R ${sequenceSequencesPath}/${theCorrectSequenceID}"
	[DefaultSymlink]="file ${sequenceSequencesPath}/${theCorrectSequenceID}/buildStrategyID1/All_Builds/${defaultStructureConformationID}"
	[EvalJsonOutput]="grep suuid ${sequenceSequencesPath}/${theCorrectSequenceID}/evaluation.json | cut -d '\"' -f4"
	[MinGasPdb]="diff ${PDB_File_To_Test} ${Subtest_0_Ref_PDB} 2>&1"
)
declare -A EvaluationCorrectOutputs
EvaluationCorrectOutputs=(
	[ListRSeqsSeqID]="""${sequenceSequencesPath}/00e7d454-06dd-5067-b6c9-441dd52db586:
buildStrategyID1
current
default
evaluation.json

${sequenceSequencesPath}/00e7d454-06dd-5067-b6c9-441dd52db586/buildStrategyID1:
All_Builds
default

${sequenceSequencesPath}/00e7d454-06dd-5067-b6c9-441dd52db586/buildStrategyID1/All_Builds:
e6c2e2e8-758b-58b8-b5ff-d138da38dd22"""
	[DefaultSymlink]="""${sequenceSequencesPath}/00e7d454-06dd-5067-b6c9-441dd52db586/buildStrategyID1/All_Builds/e6c2e2e8-758b-58b8-b5ff-d138da38dd22: symbolic link to ../../../../Builds/${evaluation_pUUID}/New_Builds/e6c2e2e8-758b-58b8-b5ff-d138da38dd22"""
	[EvalJsonOutput]="00e7d454-06dd-5067-b6c9-441dd52db586"
	[MinGasPdb]=""
)

## syntax reminder:
#for t in ${EvaluationTests[@]} ; do
#	echo "The command for test ${t} is : "
#	echo "    ${EvaluationCommands[${t}]}"
#done

