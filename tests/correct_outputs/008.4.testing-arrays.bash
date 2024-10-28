#!/usr/bin/env bash

EvaluationTests=(
	ListRBuild
	ExistingSymlink
	DiffCountJsonOutput
)
defaultConformerID="e6c2e2e8-758b-58b8-b5ff-d138da38dd22"
declare -A EvaluationCommands
EvaluationCommands=(
	[ListRBuild]="/bin/ls -R ${sequenceBuildsPath}/${eval_2_pUUID}"
	[ExistingSymlink]="file ${sequenceBuildsPath}/${eval_2_pUUID}/Existing_Builds/$defaultConformerID"
	[DiffCountJsonOutput]="diff -U 0 ${sequenceBuildsPath}/${eval_2_pUUID}/logs/response.json ${sequenceSequencesPath}/${theCorrectSequenceID}/evaluation.json | grep -v ^@ | wc -l"
)
declare -A EvaluationCorrectOutputs
EvaluationCorrectOutputs=(
    [ListRBuild]="""${sequenceBuildsPath}/${eval_2_pUUID}:
Existing_Builds
New_Builds
Requested_Builds
Sequence_Repository
default
logs

${sequenceBuildsPath}/${eval_2_pUUID}/Existing_Builds:
e6c2e2e8-758b-58b8-b5ff-d138da38dd22
logs

${sequenceBuildsPath}/${eval_2_pUUID}/Existing_Builds/logs:

${sequenceBuildsPath}/${eval_2_pUUID}/New_Builds:
logs

${sequenceBuildsPath}/${eval_2_pUUID}/New_Builds/logs:

${sequenceBuildsPath}/${eval_2_pUUID}/Requested_Builds:
e6c2e2e8-758b-58b8-b5ff-d138da38dd22

${sequenceBuildsPath}/${eval_2_pUUID}/logs:
ProjectLog.json
request-initialized.json
request-raw.json
response.json"""

	[ExistingSymlink]="""${sequenceBuildsPath}/${eval_2_pUUID}/Existing_Builds/$defaultConformerID: symbolic link to ../../../Sequences/00e7d454-06dd-5067-b6c9-441dd52db586/buildStrategyID1/All_Builds/$defaultConformerID"""

	[DiffCountJsonOutput]="28" # 28 differences between the old and new response. Dates pUUID etc.
)

## syntax reminder:
#for t in ${EvaluationTests[@]} ; do
#	echo "The command for test ${t} is : "
#	echo "    ${EvaluationCommands[${t}]}"
#done

