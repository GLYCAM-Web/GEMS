#!/bin/sh

## Shortens time spent minimizing
export GEMS_MD_TEST_WORKFLOW=True

## A place for testing output. Separated so it is safe to delete.
export GEMS_OUTPUT_PATH='/website/TESTS/git-ignore-me/pre-push'
gemsServicePath=${GEMS_OUTPUT_PATH}/sequence/cb
gemsSequencePath=${GEMS_OUTPUT_PATH}/sequence/cb/Sequences
gemsBuildPath=${GEMS_OUTPUT_PATH}/sequence/cb/Builds

## Inputs
inputJson=$GEMSHOME/gemsModules/deprecated/delegator/test_in/sequence/minimal.json
sequenceID='fc6085c0-822c-5655-b5be-88da496814cb'
now=$(date "+%Y-%m-%d-%H-%M-%S")

## Outputs
## The variable badOutDir should be defined in the calling directory.
filename=git-ignore-me_test015_out.txt
badOutput="${badOutDir}/${now}_${filename}"
File_To_Check=${gemsSequencePath}/${sequenceID}/current/All_Builds/structure/min-gas.pdb

## Edit if your machine needs more time for minimization to finish
maxTimeCount=40
sleepTime=1

clear_output()
{
	if [ -f ${badOutput} ] ; then
		#echo "Removing output."
		rm ${badOutput}
	fi
}


##################### Test 15 ########################
echo "
Testing delegator using a sequence request with a single conformer.
" | tee -a $badOutput

# See if a returned object is proper JSON and no other data
check_json_output_test() 
{
	commonServicerResponse="$(cat ${1} | python ../gemsModules/deprecated/common/utils.py)"
	if ( echo ${commonServicerResponse} | grep -q CommonServices ) ; then
		echo ""
		echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		echo ""
		echo "  The returned data is not a proper JSON Object"
		echo "  This will cause the test to fail even if the builds work."
		echo "  The Common Servicer has this to say about the data:"
		echo ""
		echo "${commonServicerResponse}"
		echo ""
		echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		echo ""
		return 1
	else
		echo "The data response appears to be ok"
		return 0
	fi
}

# Runs the script that is being tested.
run_sequenceDirectory_test() 
{
	cat $inputJson | $GEMSHOME/bin/delegate > newBuild_out.json
	check_json_output_test newBuild_out.json 
	export isJsonOk=$?
	count=0
	while [ "${count}" -lt "${maxTimeCount}" ] ; do
		sleep ${sleepTime} # Wait for it to be generated.
		if [  -e ${File_To_Check} ]; then
			break
		fi
		count=$((count+1))
		if [ "${count}" -eq "${maxTimeCount}" ] ; then
			echo "The output file was still not found after $((maxTimeCount*sleepTime)) seconds.  Aborting." | tee -a $badOutput
			echo "The output being sought is : " | tee -a $badOutput
			echo "${File_To_Check}"  | tee -a $badOutput
			echo "Test 015 FAILED!" | tee -a $badOutput
			return 1
		fi
		echo "Waited $((count*sleepTime)) seconds so far." | tee -a $badOutput
	done
	currentOutput=${File_To_Check}
	correctOutput=correct_outputs/test015.output
	if ! cmp $currentOutput $correctOutput > /dev/null 2>&1; then
		echo "Test 015 FAILED!" | tee -a $badOutput
		printf "These files are different:\n$currentOutput $correctOutput\n" | tee -a $badOutput
		if  test -e "$currentOutput"  ; then
			echo "output from test exists: $currentOutput" | tee -a $badOutput
		else
			echo "output from test is missing, expected is: $currentOutput" | tee -a $badOutput
		fi
		return 1;
	fi
	echo "Test 015 passed." 
	rm newBuild_out.json 
	clear_output
	return 0; 
}

################### MAIN #########################
#
# First remove all outputs in Builds and Sequences to test New_Builds functionality
if [ -d "${gemsServicePath}" ] ; then
	echo "Removing Sequences and Builds from ${gemsServicePath}" >> $badOutput
	( cd ${gemsServicePath} && rm -rf Sequences Builds )
else 
	mkdir -p ${gemsServicePath}
fi
if [ ! -d "${gemsServicePath}" ] ; then
	echo "Unable to create output directory.  Exiting." | tee -a $badOutput
	return 1
fi

echo "Allowing up to $((maxTimeCount*sleepTime)) seconds to complete the build." | tee -a $badOutput
echo "If your build completes, but takes longer, update the test to wait longer." | tee -a $badOutput
# Build something from scratch
if ! run_sequenceDirectory_test; then
	echo "Test 015 failed. Details can be found here: " $badOutput
	return 1;
else
	return 0;
fi

