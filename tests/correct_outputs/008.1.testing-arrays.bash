#!/usr/bin/env bash

new_conformer_id="6009ea31-3ded-57b9-aee3-2b65fe1071be"

Build1Tests=(
	ListRSeqsSeqID
	ListRRequestedBuilds
	BuildDefaultSymlink
	MinGasPdb
)

PDB_File_To_Test="${sequenceBuildsPath}/${build_1_pUUID}/New_Builds/${new_conformer_id}/min-gas.pdb"
Subtest_1_Ref_PDB="${Subtest_1_Ref_PDB_Start}/${new_conformer_id}/min-gas.pdb"

declare -A Build1Commands
Build1Commands=(
	[ListRSeqsSeqID]="/bin/ls -R ${sequenceSequencesPath}/${theCorrectSequenceID}"
	[ListRRequestedBuilds]="/bin/ls -R ${sequenceBuildsPath}/${build_1_pUUID}/Requested_Builds"
	[BuildDefaultSymlink]="file ${sequenceBuildsPath}/${build_1_pUUID}/default"
	[MinGasPdb]="md5sum ${sequenceBuildsPath}/${build_1_pUUID}/New_Builds/${new_conformer_id}/min-gas.pdb | cut -d ' ' -f1"
	[MinGasPdb]="diff ${PDB_File_To_Test} ${Subtest_1_Ref_PDB} 2>&1"
)
declare -A Build1CorrectOutputs
Build1CorrectOutputs=(
	[ListRSeqsSeqID]="""${sequenceSequencesPath}/00e7d454-06dd-5067-b6c9-441dd52db586:
buildStrategyID1
current
default
evaluation.json

${sequenceSequencesPath}/00e7d454-06dd-5067-b6c9-441dd52db586/buildStrategyID1:
All_Builds
default

${sequenceSequencesPath}/00e7d454-06dd-5067-b6c9-441dd52db586/buildStrategyID1/All_Builds:
6009ea31-3ded-57b9-aee3-2b65fe1071be
e6c2e2e8-758b-58b8-b5ff-d138da38dd22"""
	[ListRRequestedBuilds]="""${sequenceBuildsPath}/${build_1_pUUID}/Requested_Builds:
6009ea31-3ded-57b9-aee3-2b65fe1071be
e6c2e2e8-758b-58b8-b5ff-d138da38dd22"""
	[BuildDefaultSymlink]="${sequenceBuildsPath}/${build_1_pUUID}/default: symbolic link to Existing_Builds/e6c2e2e8-758b-58b8-b5ff-d138da38dd22"
	[MinGasPdb]=""
)

## syntax reminder:
#for t in ${EvaluationTests[@]} ; do
#	echo "The command for test ${t} is : "
#	echo "    ${EvaluationCommands[${t}]}"
#done

