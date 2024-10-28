#!/bin/bash
#SBATCH --chdir=/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/8a36e191-1716-4415-a21d-5c2d3d55e78e/New_Builds/ce32017d-6663-5ecc-b282-9e9812986d1c
#SBATCH --error=slurm_%x-%A.err
#SBATCH --get-user-env
#SBATCH --job-name=Glycan-8a36e191-
#SBATCH --nodes=1
#SBATCH --output=slurm_%x-%A.out
#SBATCH --partition=amber
#SBATCH --tasks-per-node=4

export MDUtilsTestRunWorkflow=Yes

/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/8a36e191-1716-4415-a21d-5c2d3d55e78e/New_Builds/ce32017d-6663-5ecc-b282-9e9812986d1c/Minimize.bash
