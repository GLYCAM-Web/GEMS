#!/bin/bash
#SBATCH --chdir=/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/f2bdcfc5-cfb4-40fa-94bf-5ba06dffea4b/New_Builds/structure
#SBATCH --error=slurm_%x-%A.err
#SBATCH --get-user-env
#SBATCH --job-name=Glycan-f2bdcfc5-
#SBATCH --nodes=1
#SBATCH --output=slurm_%x-%A.out
#SBATCH --partition=amber
#SBATCH --tasks-per-node=4

export MDUtilsTestRunWorkflow=Yes

/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/f2bdcfc5-cfb4-40fa-94bf-5ba06dffea4b/New_Builds/structure/Minimize.bash
