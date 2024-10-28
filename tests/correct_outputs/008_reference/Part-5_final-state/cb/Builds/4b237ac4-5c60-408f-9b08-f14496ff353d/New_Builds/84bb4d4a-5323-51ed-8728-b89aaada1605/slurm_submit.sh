#!/bin/bash
#SBATCH --chdir=/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/4b237ac4-5c60-408f-9b08-f14496ff353d/New_Builds/84bb4d4a-5323-51ed-8728-b89aaada1605
#SBATCH --error=slurm_%x-%A.err
#SBATCH --get-user-env
#SBATCH --job-name=Glycan-4b237ac4-
#SBATCH --nodes=1
#SBATCH --output=slurm_%x-%A.out
#SBATCH --partition=amber
#SBATCH --tasks-per-node=4

export MDUtilsTestRunWorkflow=Yes

/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/4b237ac4-5c60-408f-9b08-f14496ff353d/New_Builds/84bb4d4a-5323-51ed-8728-b89aaada1605/Minimize.bash
