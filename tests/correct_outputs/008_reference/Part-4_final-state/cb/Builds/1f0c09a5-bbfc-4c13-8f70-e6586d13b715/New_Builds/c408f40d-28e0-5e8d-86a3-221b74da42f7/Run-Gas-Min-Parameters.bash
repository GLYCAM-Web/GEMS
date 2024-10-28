#!/usr/bin/env bash

################################################################################
##
## This file holds parameters to be read into Run_Multi-Part_Simulation.bash
##
## Please see that script for documentation.
##
## Here, all parameters are explicitly set, even those left at defaults.
##
## The defaults correspond to simulations run via GLYCAM-Web.
##
## Values in this file can be overridden in a file called 
##        Local_Run_Parameters.bash
## This file is included at the bottom of this file, if it is found.
##
################################################################################

thisAMBERHOME='DETECT'
PRMTOP='unminimized-gas.parm7'
INPCRD='unminimized-gas.rst7'
initialCoordFormat='Amber7Rst'   ## Amber 7 restart
coordOutputFormat="NetCDF"  ## ntwo=2 - much smaller files; not human readable

mdEngine=sander
useMpi=N
numProcs=4
useCuda='N'
allowOverwrites='N'

writeCommands='Yes'

RunParts=( min )

declare -A Prefix
Prefix=(
	[min]='min-gas'
	)
declare -A Description
Description=(
	[min]='Minimize gas-phase structure, dielectric=80'
	)


if [ -f "Local_Run_Parameters.bash" ] ; then
	echo "found local info file"
	. Local_Run_Parameters.bash
fi
