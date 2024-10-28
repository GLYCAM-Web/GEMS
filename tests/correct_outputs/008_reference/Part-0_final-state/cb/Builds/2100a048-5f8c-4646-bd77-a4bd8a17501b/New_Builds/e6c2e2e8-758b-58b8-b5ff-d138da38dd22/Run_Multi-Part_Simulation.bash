#!/usr/bin/env bash

################################################################################
## File:  Run_Multi-Part_Simulation.bash
################################################################################
##
## This script will run one or more MD simulations for you using AMBER
##
## This script expects to find run information in a file called:
##
## 	Run_Parameters.bash
##
## ...in your current directory 
##
## You may change the filename by:
##
##      - Setting the environment variable called 'GW_RUN_PARAMETERS' so 
##        that it points to whatever file you like.
##
##      - Adding the file name (with path if needed) as an argument on the
##        command line
##
## Additionally, you may override entries in Run_Parameters.bash by creating a
## file called Local_Run_Parameters.bash
##
## Documentation of the file Run_Parameters.bash can be found in the file:
##
##	scripts/Example_Run_Parameters.bash
##
if [ "${GW_RUN_PARAMETERS}zzz" == "zzz" ] ; then
	GW_RUN_PARAMETERS="./Run_Parameters.bash"
fi
if [ "${1}zzz" != "zzz" ] ; then
	GW_RUN_PARAMETERS="${1}"
fi
##
##
################################################################################
## Some parameters must be declared.  See the Example_Run_Parameters.bash file.
################################################################################
##
################################################################################
## Parameters that have defaults start here.  These can be overridden.
################################################################################
##
##
refCoords='NONE'
thisAMBERHOME='DETECT'
PRMTOP='structure.parm7'
INPCRD='structure.rst7'
coordOutputFormat="NetCDF"  
mdEngine=pmemd
useMpi=Y
numProcs=4
useCuda=N
writeCommands=Yes
detailsFileName='details.log'
statusFileName='status.log'
allowOverwrite=Y
if [ "${coordOutputFormat}" == "NetCDF" ] ; then
	restrtSuffix='restrt.nc'
	mdSuffix='nc'
elif [ "${coordOutputFormat}" == "ASCII" ] ; then
	restrtSuffix='rst7'
	mdSuffix='mdcrd'
else
	echo "Value of coordOutputFormat variable unrecognized.  Exiting."
	exit
fi
testWorkflow=No
##
##
##
################################################################################
## This is the end of the parameters that have defaults.
##
## Normal users should not need to read or change anything below this line.
################################################################################

################################################################################
################################################################################
## First, some useful functions
##
# print_to_status_log ${Info} 
print_to_status_log() {
        if [ -z "${1}" ] ; then
		echo "Exiting - Cannot print null string to status log."
		exit 1
        else
		echo "$(date) : ${1}" >> ${statusFileName}
        fi
}
# Oliver's production step time predictor. This will break if a file name or step size changes. 
predict_time_to_complete() {
 # One could figure out the file name and pass it in, but requires saving previous step.
 # If this ever becomes an issue then figure it out then.
previousStepInfoFileName=09.relax.o
currentStepInputFileName=10.produ.in

msPerStep=$(grep "Per Step(ms)" $previousStepInfoFileName | tail -n1 | cut -d = -f 3 | sed 's/ //g') 2>/dev/null
stepsRequested=$(grep "nstlim" $currentStepInputFileName | cut -d = -f2 | sed 's/,//g' | sed 's/ //g') 2>/dev/null

checkIsNumber='^[0-9]+([.][0-9]+)?$'
if ! [[ $msPerStep =~ $checkIsNumber ]]; then
	print_to_status_log "Problem getting timing info from $previousStepInfoFileName as variable msPerStep ($msPerStep) is not a number $msPerStep"
	return 1
fi
if ! [[ $stepsRequested =~ $checkIsNumber ]]; then
        print_to_status_log "Problem getting steps requested from $currentStepInputFileName as variable stepsRequested ($stepsRequested) is not a number."
        return 1
fi

msToComplete=$(awk -va=$stepsRequested -vb=$msPerStep 'BEGIN{printf "%.2f" , a * b}')
secondsToComplete=$(awk -vm=$msToComplete 'BEGIN{printf "%.0f" , m / 1000}')
print_to_status_log "Predicted time to finish is $(( $secondsToComplete / 60 ))m $(( $secondsToComplete % 60 ))s."
}

# print_to_details_log ${Info} 
print_to_details_log() {
        if [ -z "${1}" ] ; then
		echo "Exiting - Cannot print null string to details log."
		exit 1
        else
		echo "${1}" >> ${detailsFileName}
        fi
}
# print_to_details_log ${Info} 
print_to_both_logs() {
        if [ -z "${1}" ] ; then
		echo "Exiting - Cannot print null string to the log files."
		exit 1
        else
		print_to_status_log "${1}"
                print_to_details_log "${1}"
        fi
}
# print_error_and_exit [ ${ERROR} ]
print_error_and_exit() {
        if [ -z "${1}" ] ; then
		print_to_status_log "Exiting - There was a problem. See the details file and info above." 
		print_to_details_log "Exiting - There was a problem. See the info above." 
        else
		print_to_both_logs "${1}"
        fi
        exit 1
}
# exit_if_not_array_yet_varied ${parameter}
exit_if_not_array_yet_varied() {
        if [ -z "${2}" ] ; then
		echo "number 1 is >>>${1}<<<"
		echo "number 2 is >>>${2}<<<"
		print_error_and_exit "Incorrect use of exit_if_not_array_yet_varied function"
	fi
	if [ "${1}" == "VARIED" ] ; then
		print_error_and_exit "The variable ${2} is given as VARIED, but the corresponding array is not defined."
	else
		false
	fi

}

################################################################################
################################################################################
## Simulation logic starts
##
# Start with clean logs.
echo "Details log begun on $(date)" > ${detailsFileName}
echo "Simulation setup is starting." > ${statusFileName}

if [ -f "${GW_RUN_PARAMETERS}" ] ; then
	. ${GW_RUN_PARAMETERS}
else
	print_to_details_log "The run parameters file, '${GW_RUN_PARAMETERS}', was not found."
	print_to_details_log "This file must be present. Exiting."
	print_error_and_exit "Simulation ended with GW_RUN_PARAMETERS error" 
fi
if [ "${MDUtilsTestRunWorkflow}" == "Yes" ] ; then
	testWorkflow="Yes"
fi
if [[ ${MDUtilsTestRunWorkflow} =~ ^[0-9]+$ ]] && [ "${MDUtilsTestRunWorkflow}" -gt 0 ] ; then
	testWorkflow="Yes"
	testWorkflowSteps=${MDUtilsTestRunWorkflow}
fi
if [ "${testWorkflow}"=="Yes" ] ; then
	if [ "${testWorkflowSteps}zzz" == "zzz" ] ; then
		testWorkflowSteps="1"
	fi
fi
print_to_details_log "TEST WORKFLOW IS: ${testWorkflow}"
print_to_details_log "TEST WORKFLOW STEPS IS: ${testWorkflowSteps}"

################################################################################
## Checking for parameters that must be declared.
weshouldexit="No"
if [ -z ${RunParts} ] ; then
	print_to_details_log "RunParts must be declared."
	weshouldexit="Yes"
fi
for part in ${RunParts[@]} ; do
	if [ -z "${Prefix[${part}]}" ] ; then
		print_to_details_log "The Prefix for part ${part} must be declared."
		weshouldexit="Yes"
	fi
	if [ -z "${Description[${part}]}"  ] ; then
		print_to_details_log "The Description for part ${part} must be declared."
		weshouldexit="Yes"
	fi
done
if [ "${weshouldexit}" == "Yes" ] ; then
	print_error_and_exit "Simulation ended with declarations error"
fi
##
# Start the ouput file
print_to_details_log """Beginning MD simulations on $(date)
Working directory is $(pwd) 
Using info from file: '${GW_RUN_PARAMETERS}'. """

##
##
# Source needed information from AMBERHOME
##
# First, see if an AMBERHOME is defined in the environment
if [ -z "${AMBERHOME}" ] ; then
	amberhomeDefined='No'
else
	amberhomeDefined='Yes'
fi
# If we were instructed to detect AMBERHOME, 
detectAMBERHOME='No'
if [ "${thisAMBERHOME}" == "DETECT" ] ; then 
	detectAMBERHOME='Yes'
	if [ "${amberhomeDefined}" == "Yes" ] ; then
		thisAMBERHOME=${AMBERHOME}
	else
		print_to_details_log "Could not Detect AMBERHOME.  Exiting." 
		print_error_and_exit "Simulation ended with AMBERHOME error" 
	fi
fi
if [ ! -d ${thisAMBERHOME} ] ; then
       print_to_details_log """
!!!!!!!!!!!!!!!  
Strong Warning 
!!!!!!!!!!!!!!!  
Cannot find AMBERHOME.  This is likely to cause problems if this is an attempt 
to actually run a simulation (as opposed to a test of the script, for example).
The script thinks that the following is AMBERHOME:
${thisAMBERHOME}
""" 
fi
if [ "${amberhomeDefined}" == "Yes" ] && [ "${amberhomeDefined}" != "${thisAMBERHOME}" ] ; then
	print_to_details_log "Notice: The environment defines AMBERHOME as: ${AMBERHOME}" 
fi
print_to_details_log "
This script will use the following as AMBERHOME:
AMBERHOME = ${thisAMBERHOME}
"
export AMBERHOME=${thisAMBERHOME}
if [ -e ${AMBERHOME}/amber.sh ] ; then
	SH_Output="$(source ${AMBERHOME}/amber.sh 2>&1)"
	print_to_details_log """
AMBERHOME/amber.sh was sourced.  
The output is between the two following strings of '=' signs:
===============================================================
${SH_Output}
===============================================================
"""
else
	print_to_details_log """
!!!!!!!!!!!!!!!  
Strong Warning 
!!!!!!!!!!!!!!!  
Cannot find AMBERHOME/amber.sh
This is likely to cause problems if this is an attempt to actually run a 
simulation (as opposed to a test of the script, for example).
""" 
fi

#########
######### If we made it this far, declare any undefined arrays.
#########
arrayTester="${mdEngineArr[@]}"
if [ -z "${arrayTester}" ] ; then
	exit_if_not_array_yet_varied "${mdEngine}" "mdEngine"
	declare -A MdEngineArr
fi
arrayTester="${useCudaArr[@]}"
if [ -z "${arrayTester}" ] ; then
	exit_if_not_array_yet_varied "${useCuda}" "useCuda"
	declare -A useCudaArr
fi
arrayTester="${useMpiArr[@]}"
if [ -z "${arrayTester}" ] ; then
	exit_if_not_array_yet_varied "${useMpi}" "useMpi"
	declare -A useMpiArr
fi
arrayTester="${allowOverwritesArr[@]}"
if [ -z "${arrayTester}" ] ; then
	exit_if_not_array_yet_varied "${allowOverwrites}" "allowOverwrites"
	declare -A allowOverwritesArr
fi
arrayTester="${numProcsArr[@]}"
if [ -z "${arrayTester}" ] ; then
	exit_if_not_array_yet_varied "${numProcs}" "numProcs"
	declare -A numProcsArr
fi
arrayTester="${checkTextArr[@]}"
if [ -z "${arrayTester}" ] ; then
	exit_if_not_array_yet_varied "${checkText}" "checkText"
	declare -A checkTextArr
fi
arrayTester="${useLogFileArr[@]}"
if [ -z "${arrayTester}" ] ; then
	exit_if_not_array_yet_varied "${useLogFile}" "useLogFile"
	declare -A useLogFileArr
fi
arrayTester="${refCoordsArr[@]}"
if [ -z "${refCoordsArr}" ] ; then
	exit_if_not_array_yet_varied "${refCoords}" "refCoords"
	declare -A refCoordsArr
fi

#####
##### Set the values in the arrays to the default if not already set in the arrays
#####
for part in "${RunParts[@]}" ; do
	if [ -z "${mdEngineArr[${part}]}" ] ; then
		mdEngineArr[${part}]="${mdEngine}"
	fi
	if [ -z "${useCudaArr[${part}]}" ] ; then
		useCudaArr[${part}]="${useCuda}"
	fi
	# check sanity of CUDA/engine combination
	if [ "${useCudaArr[${part}]}" == 'Y' ] ; then
		if [ "${mdEngineArr[${part}]}" != "pmemd" ] ; then 
			print_to_details_log "MD executable other than pmemd requested with CUDA.  Exiting." 
			print_error_and_exit "Simulation ended with mdEngine-CUDA error" 
		fi
	fi
	if [ -z "${useMpiArr[${part}]}" ] ; then
		useMpiArr[${part}]="${useMpi}"
	fi
	if [ -z "${allowOverwriteArr[${part}]}" ] ; then
		allowOverwriteArr[${part}]="${allowOverwrite}"
	fi
	if [ -z "${numProcsArr[${part}]}" ] ; then
		numProcsArr[${part}]="${numProcs}"
	fi
	if [ -z "${refCoordsArr[${part}]}" ] ; then
		refCoordsArr[${part}]="NONE"
	fi
	if [ -z "${checkTextArr[${part}]}" ] ; then
		if [ "${mdEngineArr[${part}]}" == "pmemd" ] ; then 
			checkTextArr[${part}]='Total wall time'
		elif [ "${mdEngineArr[${part}]}" == "sander" ] ; then 
			checkTextArr[${part}]='wallclock() was called'
		else
			print_to_details_file "mdEngine other than pmemd or sander was specified without specifying a normal finish text." 
			print_error_and_exit "Simulation ended with checkTextArr error" 
		fi
	fi
	if [ -z "${useLogFileArr[${part}]}" ] ; then
		if [ "${mdEngineArr[${part}]}" == "pmemd" ] ; then 
			useLogFileArr[${part}]='Y'
		else
			useLogFileArr[${part}]='N'
		fi
	fi

done

#####
##### Start building the commands
#####
print_to_details_log "
There will be ${#RunParts[@]} phases to this simulation: 
"
print_to_status_log "Simulation will run with ${#RunParts[@]} phases" 

declare -A Commands
thisRestart="${INPCRD}"
i=1
for part in "${RunParts[@]}" ; do
	print_to_details_log """Phase ${i} 
	- is called ${part} 
	- has prefix ${Prefix[${part}]} 
	- is described as: ${Description[${part}]}""" 

	thisMdEngine="${mdEngineArr[${part}]}"

	if [ "${useCudaArr[${part}]}" == "Y" ] ; then 
		thisMdEngine="${thisMdEngine}.cuda"
	fi

	if [ "${useMpiArr[${part}]}" == "Y" ] ; then 
		thisMdEngine="mpirun ${thisMdEngine}.MPI -np ${numProcsArr[${part}]} "
	fi

	if [ "${allowOverwriteArr[${part}]}" == "Y" ] ; then 
		thisMdEngine="${thisMdEngine} -O "
	fi


	COMMAND="${thisMdEngine} \
 -i ${Prefix[${part}]}.in \
 -o ${Prefix[${part}]}.o \
 -e ${Prefix[${part}]}.en \
 -p ${PRMTOP} \
 -c ${thisRestart} \
 -r ${Prefix[${part}]}.${restrtSuffix} \
 -x ${Prefix[${part}]}.${mdSuffix} \
 -inf ${Prefix[${part}]}.info "

	if [ "${useLogFileArr[${part}]}" == "Y" ] ; then
		COMMAND="${COMMAND} -l ${Prefix[${part}]}.log "
	fi

	if [ "${refCoordsArr[${part}]}" != "NONE" ] ; then
		if [ "${refCoordsArr[${part}]}" == "Initial" ] ; then
			thisRefCoords="${INPCRD}"
		else
			thisRefPart="${refCoordsArr[${part}]}"
			thisRefCoords="${Prefix[${thisRefPart}]}.${restrtSuffix}"
		fi
		COMMAND="${COMMAND} -ref ${thisRefCoords}"
	fi

	Commands[${part}]="${COMMAND}"

	thisRestart=${Prefix[${part}]}.${restrtSuffix}

	i=$((i+1))
done

for part in ${RunParts[@]} ; do
	echo "This is the command for part ${part}"
	echo "${Commands[${part}]}"
done

#echo "COMMENT OUT THIS LINE AND THE EXIT COMMAND NEXT"
#exit



print_to_status_log "Simulation setup is complete." 
if [ "${writeCommands}" != "Only" ] ; then
	print_to_status_log "Starting the ${#RunParts[@]} phases of this simulation." 
else
	print_to_status_log "Writing commands only for the ${#RunParts[@]} phases of this simulation." 
fi

##  Do the runs
#
AllRunsOk="Yes"
for part in ${RunParts[@]} ; do
	print_to_details_log "
	Starting phase ${part}" 

	COMMAND="${Commands[${part}]}"
	
	if [ "${testWorkflow}" == "Yes" ] ; then
		if [ ! -f "${Prefix[${part}]}.in.original" ] ; then
			cp "${Prefix[${part}]}.in" "${Prefix[${part}]}.in.original"
		fi

		steps="${testWorkflowSteps}"
		sed -i s/maxcyc\ *=\ *[1-9][0-9]*/maxcyc\ =\ ${steps}/ ${Prefix[${part}]}.in 
		sed -i s/ncyc\ *=\ *[1-9][0-9]*/ncyc\ =\ ${steps}/ ${Prefix[${part}]}.in 
		sed -i s/nstlim\ *=\ *[1-9][0-9]*/nstlim\ =\ ${steps}/ ${Prefix[${part}]}.in 
		sed -i s/ntpr\ *=\ *[1-9][0-9]*/ntpr\ =\ ${steps}/ ${Prefix[${part}]}.in 
		sed -i s/ntwe\ *=\ *[1-9][0-9]*/ntwe\ =\ ${steps}/ ${Prefix[${part}]}.in 
		sed -i s/ntwx\ *=\ *[1-9][0-9]*/ntwx\ =\ ${steps}/ ${Prefix[${part}]}.in 
		sed -i -E s/ntwr\ *=\ *-?[1-9][0-9]*/ntwr\ =\ ${steps}/ ${Prefix[${part}]}.in 
	fi
	#
	#  Write it to a file if desired
	if [ "${writeCommands}" != "No" ] ; then
		print_to_details_log "
		The command is:
		${COMMAND}

		" 
	fi
	#
	#  Run the command unless told not to 
	if [ "${writeCommands}" != "Only" ] ; then
		print_to_status_log "Starting phase ${part}." >> ${statusFileName}
		SECONDS=0 # Oliver adding timing. SECONDS will increment by itself. See SECONDS usage below.
		#Oliver timing prediction for produ
		if [ "${part}" == "produ10" ]; then
		    predict_time_to_complete
		fi
		eval ${COMMAND}
		#
		# Check if the command worked
		if ! grep -q "${checkTextArr[${part}]}" ${Prefix[${part}]}.o ; then
			print_to_details_log "

Something went wrong for run phase ${part}.
The simulation cannot continue.  
"  
			print_to_status_log "Simulation has failed on phase ${part}." 
			print_error_and_exit "Simulation finished with MD error." 
		fi
		print_to_both_logs "Phase ${part} finished normally after $(( SECONDS / 60 ))m $(( SECONDS % 60 ))s." 
	fi

done

print_to_both_logs "Simulation finished normally." 
