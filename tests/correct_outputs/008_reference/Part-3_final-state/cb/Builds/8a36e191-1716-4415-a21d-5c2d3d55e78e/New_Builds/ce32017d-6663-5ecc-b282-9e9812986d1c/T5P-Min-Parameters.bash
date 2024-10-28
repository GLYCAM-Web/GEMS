#!/usr/bin/env bash

################################################################################
##
## This file holds parameters to be read into Run_Multi-Part_Simulation.bash
##
## Please see that script for documentation.
##
## Here, all parameters are explicitly set, even those left at defaults.
##
################################################################################

thisAMBERHOME='DETECT'
PRMTOP='unminimized-t5p.parm7'
INPCRD='unminimized-t5p.rst7'
coordOutputFormat="NetCDF"  ## ntwo=2 - much smaller files; not human readable
restrtSuffix='restrt.nc'
mdSuffix='nc'
outputFileName='t5p_minimization.log'

mdEngine=pmemd
useMpi=Y
numProcs=4
useCuda=N
allowOverwrites=N

writeCommands=Yes

runPrefix[0]='min-t5p'
runDescription[0]='T5P-solvated minimization'
