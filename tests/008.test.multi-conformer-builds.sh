#!/bin/sh

# If GEMS_KEEP_BAD_OUTPUTS is set to "True", badOutputs will not be removed after testing

. './utilities/common_environment.bash'
. './utilities/functions.bash'

echo "The output path is: ${GEMS_OUTPUT_PATH}"

## The variable badOutDir should be defined in the script that calls this one.
outputFilePrefix='git-ignore-me_test008'
badOutputPrefix="${badOutDir}/${now}_${outputFilePrefix}"
badOutput="${badOutputPrefix}.txt"

ALL_JSON_ARE_GOOD='true'
ALL_TESTS_PASSED='true'

theCorrectSequenceID='00e7d454-06dd-5067-b6c9-441dd52db586'
defaultStructureConformationID='e6c2e2e8-758b-58b8-b5ff-d138da38dd22'

evaluation_input="${GEMSHOME}/tests/inputs/008.0.evaluation-request.json"
build_1_input="${GEMSHOME}/tests/inputs/008.1.build-request-first-two.json"
build_2_input="${GEMSHOME}/tests/inputs/008.2.build-request-second-two.json"
build_3_input="${GEMSHOME}/tests/inputs/008.3.build-request-third-four.json"
build_5_input="${GEMSHOME}/tests/inputs/008.5.build-request-NotDefault.json"
build_6_input="${GEMSHOME}/tests/inputs/008.6.build-request-NoRotamers.json"

source 'correct_outputs/008_reference_data.bash'

do_the_common_tasks() {	
	jsonInFile="${1}"
	outFilePrefix="${2}"
	theJsonFile=${outFilePrefix}.json
	#echo "the out file is : ${theJsonFile}"

	# Delegate the json input

	theJsonOut="$(cat ${jsonInFile} | $GEMSHOME/bin/delegate | tee ${theJsonFile})"

	check_output_is_only_json ${theJsonFile}
	
	isJsonOk=$?
	
	if [ "${isJsonOk}" != 0 ] ; then
		ALL_JSON_ARE_GOOD='false'
		echo "FAILURE:  ${1} got a non-purely-json response from delegator." | tee -a ${badOutput}
		echo "Check ${theJsonFile} for more information." | tee -a ${badOutput}
	fi

	get_seqID_from_json ${theJsonFile}
	if [ "${theseqID}" != "${theCorrectSequenceID}" ] ; then
		ALL_SEQID_ARE_GOOD='false'
		echo "FAILURE:  got seqID of ${theseqID} which shouldbe ${theCorrectSequenceID}." | tee -a ${badOutput}
	fi
	export theseqID

	get_pUUID_from_json ${theJsonFile}
	export thepUUID
	return 0
}

copyTestOutputDirectoryTree()
{	# Remove all outputs in Builds and Sequences to test New_Builds functionality
	#  $1 should be an integer, 0-6, corresponding to the subtest
	echo "Copying the output directory, if it exists, to the badOut directory."
	if [ ! -d "${sequenceServicePath}" ] ; then
	    echo "Outputs directory not found:  ${sequenceServicePath}" >> $badOutput
        else
    	    mkdir -p ${badOutDir}/${now}/${1}
    	    cp -a ${sequenceServicePath} ${badOutDir}/${now}/${1}/
        fi
    	return 0
}

deleteTestOutputFolders()
{	# Remove all outputs in Builds and Sequences to test New_Builds functionality
	echo "Checking for sequence service path."
	if [ -d "${sequenceServicePath}" ] ; then
	    echo "Removing Sequences and Builds from ${sequenceServicePath}" >> $badOutput
    	( cd ${sequenceServicePath} && rm -rf Sequences Builds )
    	return 0
    fi
   	mkdir -p ${sequenceServicePath} | tee -a $badOutput
}

################### MAIN #########################
deleteTestOutputFolders
echo """
################################################################################
## Sub test 0:  Evaluation
################################################################################"""
source './sub_parts/008.0.sub-test.bash'
copyTestOutputDirectoryTree 0


if [ "${ALL_TESTS_PASSED}" == "true" ] ; then
	echo """
################################################################################
## Sub test 1:  build first two conformers
################################################################################"""
	source './sub_parts/008.1.sub-test.bash'
	copyTestOutputDirectoryTree 1
fi

if [ "${ALL_TESTS_PASSED}" == "true" ] ; then
	echo """
################################################################################
## Sub test 2:  build two more two conformers
################################################################################"""
	source './sub_parts/008.2.sub-test.bash'
	copyTestOutputDirectoryTree 2
fi

if [ "${ALL_TESTS_PASSED}" == "true" ] ; then
	echo """
################################################################################
## Sub test 3:  build two new and two existing conformers
################################################################################"""
	source './sub_parts/008.3.sub-test.bash'
	copyTestOutputDirectoryTree 3
fi

if [ "${ALL_TESTS_PASSED}" == "true" ] ; then
    echo """
################################################################################
## Sub test 4:  Do the Evaluation again.
################################################################################"""
	source './sub_parts/008.4.sub-test.bash'
	copyTestOutputDirectoryTree 4
fi

if [ "${ALL_TESTS_PASSED}" == "true" ] ; then
    echo """
################################################################################
## Sub test 5:  Clean and then request structures where none are the default. 
################################################################################"""
    deleteTestOutputFolders
    source './sub_parts/008.0.sub-test.bash' # Must do an evaluation first because bugs.
    source './sub_parts/008.5.sub-test.bash'
    copyTestOutputDirectoryTree 5
fi

if [ "${ALL_TESTS_PASSED}" == "true" ] ; then
    echo """
################################################################################
## Sub test 6:  Request with no rotamers. 
################################################################################"""
    deleteTestOutputFolders
    source './sub_parts/008.6.sub-test.bash'
    copyTestOutputDirectoryTree 6
fi


if [ "${ALL_JSON_ARE_GOOD}" == "false" ] ; then
        echo "The builds worked, but one or more JSON delegations FAILED."
	ALL_TESTS_PASSED='false'
fi
if [ "${ALL_TESTS_PASSED}" == "false" ] ; then
		return 1;
fi
## Clean up.
deleteTestOutputFolders
if [ ${GEMS_KEEP_BAD_OUTPUTS} != "True" ] ; then
	remove_file_if_found ${badOutput}
fi
return 0;
