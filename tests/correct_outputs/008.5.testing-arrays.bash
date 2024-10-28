#!/usr/bin/env bash

test_conformer_id1='6009ea31-3ded-57b9-aee3-2b65fe1071be'
test_conformer_id2='84bb4d4a-5323-51ed-8728-b89aaada1605'
oldDefault_conformerId='e6c2e2e8-758b-58b8-b5ff-d138da38dd22'

PDB_File_To_Test="${sequenceBuildsPath}/${build_5_pUUID}/New_Builds/${test_conformer_id1}/min-gas.pdb"
Subtest_5_Ref_PDB="${Subtest_5_Ref_PDB_Start}/${test_conformer_id1}/min-gas.pdb"
# [MinGasPdb]="md5sum ${sequenceBuildsPath}/${build_5_pUUID}/New_Builds/${test_conformer_id1}/min-gas.pdb | cut -d ' ' -f1"
# [MinGasPdb]="e5652a887b3f7a75228ab9d0a744e735"
Build5Tests=(
	ListRSeqsSeqID
	MinGasPdb
	treeBuildProject
)
declare -A Build5Commands
Build5Commands=(
    [treeBuildProject]="tree -id ${sequenceBuildsPath}/${build_5_pUUID}"
	[ListRSeqsSeqID]="/bin/ls -R ${sequenceSequencesPath}/${theCorrectSequenceID}"
	
	[BuildDefaultSymlink]="file ${sequenceBuildsPath}/${build_5_pUUID}/default"
	[MinGasPdb]="diff ${PDB_File_To_Test} ${Subtest_5_Ref_PDB} 2>&1"
)
declare -A Build5CorrectOutputs
Build5CorrectOutputs=(
	[ListRSeqsSeqID]="""${sequenceSequencesPath}/00e7d454-06dd-5067-b6c9-441dd52db586:
buildStrategyID1
current
default
evaluation.json

${sequenceSequencesPath}/${theCorrectSequenceID}/buildStrategyID1:
All_Builds
default

${sequenceSequencesPath}/${theCorrectSequenceID}/buildStrategyID1/All_Builds:
${test_conformer_id1}
${test_conformer_id2}
${oldDefault_conformerId}"""
	[MinGasPdb]=""
	[treeBuildProject]="""${sequenceBuildsPath}/${build_5_pUUID}
Existing_Builds
logs
New_Builds
${test_conformer_id1}
${test_conformer_id2}
logs
Requested_Builds
${test_conformer_id1} -> ../New_Builds/${test_conformer_id1}
${test_conformer_id2} -> ../New_Builds/${test_conformer_id2}
Sequence_Repository -> ../../Sequences/${theCorrectSequenceID}
default -> New_Builds/${test_conformer_id1}
logs

12 directories"""
)

## syntax reminder:
#for t in ${EvaluationTests[@]} ; do
#	echo "The command for test ${t} is : "
#	echo "    ${EvaluationCommands[${t}]}"
#done

