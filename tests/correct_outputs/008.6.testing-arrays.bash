#!/usr/bin/env bash

test_conformer_id='structure'
theCorrectSequenceID='fc6085c0-822c-5655-b5be-88da496814cb'
Build6Tests=(
	treeEverything
	BuildDefaultSymlink
	MinGasPdb
)
declare -A Build6Commands=(
	[MinGasPdb]="md5sum ${sequenceBuildsPath}/${build_6_pUUID}/New_Builds/${test_conformer_id}/min-gas.pdb | cut -d ' ' -f1"
	[BuildDefaultSymlink]="file ${sequenceBuildsPath}/${build_6_pUUID}/default"
	[treeEverything]="tree -id ${sequenceServicePath}/"
	)
declare -A Build6CorrectOutputs=(
	[MinGasPdb]="6777b0c68693350a0dda66ab87f92831"
	[BuildDefaultSymlink]="${sequenceBuildsPath}/${build_6_pUUID}/default: symbolic link to New_Builds/$test_conformer_id"
    [treeEverything]="""/website/TESTS/git-ignore-me/pre-push/sequence/cb/
Builds
${build_6_pUUID}
Existing_Builds
logs
New_Builds
logs
structure
Requested_Builds
structure -> ../New_Builds/structure
Sequence_Repository -> ../../Sequences/${theCorrectSequenceID}
default -> New_Builds/structure
logs
Sequences
${theCorrectSequenceID}
buildStrategyID1
All_Builds
structure -> ../../../../Builds/${build_6_pUUID}/New_Builds/structure
default -> All_Builds/structure
current -> buildStrategyID1
default -> buildStrategyID1/All_Builds/structure

20 directories"""
)

## syntax reminder:
#for t in ${EvaluationTests[@]} ; do
#	echo "The command for test ${t} is : "
#	echo "    ${EvaluationCommands[${t}]}"
#done

