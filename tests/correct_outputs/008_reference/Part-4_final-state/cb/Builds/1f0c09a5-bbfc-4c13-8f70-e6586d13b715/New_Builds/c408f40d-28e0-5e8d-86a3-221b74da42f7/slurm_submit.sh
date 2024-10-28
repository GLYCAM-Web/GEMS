#!/bin/bash
#SBATCH --chdir=/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/1f0c09a5-bbfc-4c13-8f70-e6586d13b715/New_Builds/c408f40d-28e0-5e8d-86a3-221b74da42f7
#SBATCH --error=slurm_%x-%A.err
#SBATCH --get-user-env
#SBATCH --job-name=Glycan-1f0c09a5-
#SBATCH --nodes=1
#SBATCH --output=slurm_%x-%A.out
#SBATCH --partition=amber
#SBATCH --tasks-per-node=4

export MDUtilsTestRunWorkflow=Yes

/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/1f0c09a5-bbfc-4c13-8f70-e6586d13b715/New_Builds/c408f40d-28e0-5e8d-86a3-221b74da42f7/Minimize.bash
