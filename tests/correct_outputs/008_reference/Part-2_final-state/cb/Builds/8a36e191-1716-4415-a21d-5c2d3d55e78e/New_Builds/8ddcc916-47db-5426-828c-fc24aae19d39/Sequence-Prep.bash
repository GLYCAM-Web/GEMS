#!/usr/bin/env bash

################################################################################
##
## This file performs the standard build and minimization for glycans
## built using the tools at GLYCAM-Web and associated software.
##
## AMBERHOME must be either:
##     *  set as an environment variable.
##     *  set in a file called 'Minimize-Parameters.bash'
##
## The following parameters may be overridden in Minimize-Parameters.bash
LOGFILE='Sequence-Prep-details.log'  ## Log file is very chatty, for tracking problems
STATUSFILE='Sequence-Prep-status.log'  ## Status file is terse, with date/time stamps each line
##
## The following parameters may be overridden:
##     *  in Minimize-Parameters.bash
##     *  by setting an environment variable.
##           Note that the environment variable has a different name.
##
# Set this one to 'Yes' if you don't want to perform a full simulation but
# just want to make sure the workflow functions.  This makes the MD sims only
# run for a single step each.
testWorkflow=No   ## Environment variable:  MDUtilsTestRunWorkflow
# testWorkflow=Yes   
##
################################################################################

if [ -f Minimize-Parameters.bash ] ; then
	. Minimize-Parameters.bash
fi
# Pass workflow information along if needed
if [ "${MDUtilsTestRunWorkflow}" == "Yes" ] ; then
	export MDUtilsTestRunWorkflow=Yes
fi
if [ "${testWorkflow}" == "Yes" ] ; then
	export MDUtilsTestRunWorkflow=Yes
fi

write_return_value_info_to_log_status()
{
	Val="${1}"  ## the return value
	Mess="${2}"  ## the action message
	if [ "${Val}" != "0" ] ; then
		echo "...${Mess} failed with code ${Val}.  Exiting" >> ${LOGFILE}
		echo "[ERROR] - $(date) - ${Mess} failed with code ${Val}" >> ${STATUSFILE}
		exit 1
	else
		echo "...${Mess} completed on $(date)" >> ${LOGFILE}
		echo "[INFO] - $(date) - ${Mess} completed" >> ${STATUSFILE}
	fi
}
run_command_and_log_results()
{
	echo "${1} " >> ${LOGFILE}
        eval "${2}  >> ${LOGFILE} 2>&1"
	returnValue=$?
	write_return_value_info_to_log_status "${returnValue}" "${3}"
}


###  Initialize the log and status files
echo "Run log begun on $(date) " > ${LOGFILE}
echo "[INFO] - $(date) - Status log opened." > ${STATUSFILE}

###  If we seem to be in a Slurm cluster, record some info
( 
command -V srun >/dev/null 2>&1 &&
  ( 
  echo "This build appears to be running in a Slurm cluster.:" >> ${LOGFILE} 
  echo "The current host is $(hostname):" >> ${LOGFILE} 
  echo "The build will run on these hosts:" >> ${LOGFILE} 
  echo "[INFO] - $(date) - This job is running in a Slurm cluster." >> ${STATUSFILE}
  srun hostname -s | sort -u >slurm.hosts
  cat slurm.hosts >> ${LOGFILE}
  )
)

run_command_and_log_results \
	"Sourcing amber.sh" \
	"source ${AMBERHOME}/amber.sh" \
	"Sourcing of AMBERHOME[=${AMBERHOME}]/amber.sh"

echo "
Building and minimizing the gas-phase system.
" >> ${LOGFILE}

run_command_and_log_results \
	"Running tleap to generate gas-phase input files." \
	"tleap -f unminimized-gas.leapin" \
	'Gas-phase tleap processing'

run_command_and_log_results \
	"Running the Gas-Phase Minimization"  \
	"bash Run_Multi-Part_Simulation.bash Run-Gas-Min-Parameters.bash" \
	'Gas-phase minimization'

echo "
NOT building and minimizing the solvated systems.
" >> ${LOGFILE}

run_command_and_log_results \
	"Running cpptraj to convert gas-phase output to convenient formats"  \
	"cpptraj -i min-gas.cpptrajin" \
	'Post-gas-phase cpptraj processing'

echo "
Working on TIP3P solvated version.
" >> ${LOGFILE}

run_command_and_log_results \
	"Running tleap to build the Tip3P solvated structures"  \
	"tleap -f unminimized-t3p.leapin" \
	'Solvent-phase (T3P) tleap processing'

#run_command_and_log_results \
#	"Running the Tip3P-Solvated Minimization" \
#	"bash Run_Multi-Part_Simulation.bash T3P-Min-Parameters.bash" \
#	'Solvent-phase (T3P) minimization'

#run_command_and_log_results \
#	"Running cpptraj to convert t3p-solvated output to convenient formats"  \
#	"cpptraj -i min-t3p.cpptrajin" \
#	'Post-t3p-solvated cpptraj processing'

echo "
Working on TIP5P solvated version.
" >> ${LOGFILE}

run_command_and_log_results \
	"Running tleap to build the Tip5P solvated structures"  \
	"tleap -f unminimized-t5p.leapin " \
	'Solvent-phase (T5P) tleap processing'

#run_command_and_log_results \
#	"Running the Tip5P-Solvated Minimization" \
#	"bash Run_Multi-Part_Simulation.bash T5P-Min-Parameters.bash" \
#	'Solvent-phase (T5P) minimization'

#run_command_and_log_results \
#	"Running cpptraj to convert t5p-solvated output to convenient formats"  \
#	"cpptraj -i min-t5p.cpptrajin" \
#	'Post-t5p-solvated cpptraj processing'

echo "
Got to end of $0
" >> ${LOGFILE}
