#!/bin/bash
#SBATCH --chdir=/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/3561e3cd-4ce7-40ee-afb5-b603a1717d9a/New_Builds/6009ea31-3ded-57b9-aee3-2b65fe1071be
#SBATCH --error=slurm_%x-%A.err
#SBATCH --get-user-env
#SBATCH --job-name=Glycan-3561e3cd-
#SBATCH --nodes=1
#SBATCH --output=slurm_%x-%A.out
#SBATCH --partition=amber
#SBATCH --tasks-per-node=4

export MDUtilsTestRunWorkflow=Yes

/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/3561e3cd-4ce7-40ee-afb5-b603a1717d9a/New_Builds/6009ea31-3ded-57b9-aee3-2b65fe1071be/Minimize.bash
