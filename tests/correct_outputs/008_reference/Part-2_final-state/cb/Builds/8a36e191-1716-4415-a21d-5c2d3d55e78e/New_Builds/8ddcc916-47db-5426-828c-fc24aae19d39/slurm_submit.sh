#!/bin/bash
#SBATCH --chdir=/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/8a36e191-1716-4415-a21d-5c2d3d55e78e/New_Builds/8ddcc916-47db-5426-828c-fc24aae19d39
#SBATCH --error=slurm_%x-%A.err
#SBATCH --get-user-env
#SBATCH --job-name=Glycan-8a36e191-
#SBATCH --nodes=1
#SBATCH --output=slurm_%x-%A.out
#SBATCH --partition=amber
#SBATCH --tasks-per-node=4

export MDUtilsTestRunWorkflow=Yes

/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/8a36e191-1716-4415-a21d-5c2d3d55e78e/New_Builds/8ddcc916-47db-5426-828c-fc24aae19d39/Minimize.bash
